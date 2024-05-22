# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class UnknownResponseEvent:
    """
    Reply that could not be matched to a request.
    """

    device_address: int
    """
    Number of the device that sent or should receive the message.
    """

    command: int
    """
    The warning flag contains the highest priority warning currently active for the device or axis.
    """

    data: int
    """
    Data payload of the message, if applicable, or zero otherwise.
    """

    @staticmethod
    def zero_values() -> 'UnknownResponseEvent':
        return UnknownResponseEvent(
            device_address=0,
            command=0,
            data=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnknownResponseEvent':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnknownResponseEvent.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceAddress': self.device_address,
            'command': self.command,
            'data': self.data,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnknownResponseEvent':
        return UnknownResponseEvent(
            device_address=data.get('deviceAddress'),  # type: ignore
            command=data.get('command'),  # type: ignore
            data=data.get('data'),  # type: ignore
        )
