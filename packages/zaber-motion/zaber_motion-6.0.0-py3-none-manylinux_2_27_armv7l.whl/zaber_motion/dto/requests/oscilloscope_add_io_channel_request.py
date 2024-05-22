# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.io_port_type import IoPortType


@dataclass
class OscilloscopeAddIoChannelRequest:

    interface_id: int = 0

    device: int = 0

    io_type: IoPortType = next(first for first in IoPortType)

    io_channel: int = 0

    @staticmethod
    def zero_values() -> 'OscilloscopeAddIoChannelRequest':
        return OscilloscopeAddIoChannelRequest(
            interface_id=0,
            device=0,
            io_type=next(first for first in IoPortType),
            io_channel=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OscilloscopeAddIoChannelRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OscilloscopeAddIoChannelRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'ioType': self.io_type.value,
            'ioChannel': self.io_channel,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OscilloscopeAddIoChannelRequest':
        return OscilloscopeAddIoChannelRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            io_type=IoPortType(data.get('ioType')),  # type: ignore
            io_channel=data.get('ioChannel'),  # type: ignore
        )
