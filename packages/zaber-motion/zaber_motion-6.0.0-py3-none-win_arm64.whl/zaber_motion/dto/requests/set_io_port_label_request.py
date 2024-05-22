# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.io_port_type import IoPortType


@dataclass
class SetIoPortLabelRequest:

    interface_id: int = 0

    device: int = 0

    port_type: IoPortType = next(first for first in IoPortType)

    channel_number: int = 0

    label: str = ""

    @staticmethod
    def zero_values() -> 'SetIoPortLabelRequest':
        return SetIoPortLabelRequest(
            interface_id=0,
            device=0,
            port_type=next(first for first in IoPortType),
            channel_number=0,
            label="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetIoPortLabelRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetIoPortLabelRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'portType': self.port_type.value,
            'channelNumber': self.channel_number,
            'label': self.label,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetIoPortLabelRequest':
        return SetIoPortLabelRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            port_type=IoPortType(data.get('portType')),  # type: ignore
            channel_number=data.get('channelNumber'),  # type: ignore
            label=data.get('label'),  # type: ignore
        )
