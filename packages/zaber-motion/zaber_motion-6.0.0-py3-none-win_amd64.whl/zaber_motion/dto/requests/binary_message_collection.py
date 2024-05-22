# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..binary.message import Message


@dataclass
class BinaryMessageCollection:

    messages: List[Message] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'BinaryMessageCollection':
        return BinaryMessageCollection(
            messages=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryMessageCollection':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryMessageCollection.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'messages': [item.to_dict() for item in self.messages],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryMessageCollection':
        return BinaryMessageCollection(
            messages=[Message.from_dict(item) for item in data.get('messages')],  # type: ignore
        )
