# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class CommandTooLongExceptionData:
    """
    Information describing why the command could not fit.
    """

    fit: str
    """
    The part of the command that could be successfully fit in the space provided by the protocol.
    """

    remainder: str
    """
    The part of the command that could not fit within the space provided.
    """

    packet_size: int
    """
    The length of the ascii string that can be written to a single line.
    """

    packets_max: int
    """
    The number of lines a command can be split over using continuations.
    """

    @staticmethod
    def zero_values() -> 'CommandTooLongExceptionData':
        return CommandTooLongExceptionData(
            fit="",
            remainder="",
            packet_size=0,
            packets_max=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CommandTooLongExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CommandTooLongExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'fit': self.fit,
            'remainder': self.remainder,
            'packetSize': self.packet_size,
            'packetsMax': self.packets_max,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CommandTooLongExceptionData':
        return CommandTooLongExceptionData(
            fit=data.get('fit'),  # type: ignore
            remainder=data.get('remainder'),  # type: ignore
            packet_size=data.get('packetSize'),  # type: ignore
            packets_max=data.get('packetsMax'),  # type: ignore
        )
