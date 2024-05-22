# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..binary.reply_only_event import ReplyOnlyEvent


@dataclass
class BinaryReplyOnlyEventWrapper:

    interface_id: int = 0

    reply: ReplyOnlyEvent = field(default_factory=ReplyOnlyEvent.zero_values)

    @staticmethod
    def zero_values() -> 'BinaryReplyOnlyEventWrapper':
        return BinaryReplyOnlyEventWrapper(
            interface_id=0,
            reply=ReplyOnlyEvent.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryReplyOnlyEventWrapper':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryReplyOnlyEventWrapper.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'reply': self.reply.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryReplyOnlyEventWrapper':
        return BinaryReplyOnlyEventWrapper(
            interface_id=data.get('interfaceId'),  # type: ignore
            reply=ReplyOnlyEvent.from_dict(data.get('reply')),  # type: ignore
        )
