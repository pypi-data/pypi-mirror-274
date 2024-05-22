# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .io_port_type import IoPortType


@dataclass
class IoPortLabel:
    """
    The label of an IO port.
    """

    port_type: IoPortType
    """
    The type of the port.
    """

    channel_number: int
    """
    The number of the port.
    """

    label: str
    """
    The label of the port.
    """

    @staticmethod
    def zero_values() -> 'IoPortLabel':
        return IoPortLabel(
            port_type=next(first for first in IoPortType),
            channel_number=0,
            label="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'IoPortLabel':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return IoPortLabel.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'portType': self.port_type.value,
            'channelNumber': self.channel_number,
            'label': self.label,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'IoPortLabel':
        return IoPortLabel(
            port_type=IoPortType(data.get('portType')),  # type: ignore
            channel_number=data.get('channelNumber'),  # type: ignore
            label=data.get('label'),  # type: ignore
        )
