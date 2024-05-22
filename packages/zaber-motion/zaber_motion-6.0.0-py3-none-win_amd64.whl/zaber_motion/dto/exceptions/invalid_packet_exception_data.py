# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class InvalidPacketExceptionData:
    """
    Contains additional data for the InvalidPacketException.
    """

    packet: str
    """
    The invalid packet that caused the exception.
    """

    reason: str
    """
    The reason for the exception.
    """

    @staticmethod
    def zero_values() -> 'InvalidPacketExceptionData':
        return InvalidPacketExceptionData(
            packet="",
            reason="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'InvalidPacketExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return InvalidPacketExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'packet': self.packet,
            'reason': self.reason,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'InvalidPacketExceptionData':
        return InvalidPacketExceptionData(
            packet=data.get('packet'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
        )
