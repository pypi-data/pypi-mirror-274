# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TranslateMessage:
    """
    Represents a message from translator regarding a block translation.
    """

    message: str
    """
    The message describing an occurrence.
    """

    from_block: int
    """
    The index in the block string that the message regards to.
    """

    to_block: int
    """
    The end index in the block string that the message regards to.
    The end index is exclusive.
    """

    @staticmethod
    def zero_values() -> 'TranslateMessage':
        return TranslateMessage(
            message="",
            from_block=0,
            to_block=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslateMessage':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslateMessage.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'message': self.message,
            'fromBlock': self.from_block,
            'toBlock': self.to_block,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslateMessage':
        return TranslateMessage(
            message=data.get('message'),  # type: ignore
            from_block=data.get('fromBlock'),  # type: ignore
            to_block=data.get('toBlock'),  # type: ignore
        )
