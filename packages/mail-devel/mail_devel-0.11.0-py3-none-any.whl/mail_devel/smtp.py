import logging
import uuid
from email.message import Message
from typing import Type

from aiosmtpd.handlers import AsyncMessage
from pymap.parsing.specials.flag import Flag

from .mailbox import TestMailboxDict

_logger = logging.getLogger(__name__)


class MemoryHandler(AsyncMessage):
    def __init__(
        self,
        mailboxes: TestMailboxDict,
        flagged_seen: bool = False,
        ensure_message_id: bool = True,
        message_class: Type[Message] | None = None,
        multi_user: bool = False,
    ):
        super().__init__(message_class)
        self.mailboxes: TestMailboxDict = mailboxes
        self.flagged_seen: bool = flagged_seen
        self.ensure_message_id = ensure_message_id
        self.multi_user: bool = multi_user

    def prepare_message(self, session, envelope):
        if envelope.smtp_utf8 and isinstance(envelope.content, (bytes, bytearray)):
            data = envelope.content
            try:
                envelope.content = data.decode()
            except UnicodeError:
                pass
        return super().prepare_message(session, envelope)

    async def handle_message(self, message: Message) -> None:  # type: ignore
        _logger.info(f"Got message {message['From']} -> {message['To']}")
        if not message["Message-Id"] and self.ensure_message_id:
            message.add_header("Message-Id", f"{uuid.uuid4()}@mail-devel")

        await self.mailboxes.append(
            message,
            flags=frozenset({Flag(b"\\Seen")} if self.flagged_seen else []),
        )
