# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceGetAnalogIORequest:

    interface_id: int = 0

    device: int = 0

    channel_type: str = ""

    channel_number: int = 0

    @staticmethod
    def zero_values() -> 'DeviceGetAnalogIORequest':
        return DeviceGetAnalogIORequest(
            interface_id=0,
            device=0,
            channel_type="",
            channel_number=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceGetAnalogIORequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceGetAnalogIORequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'channelType': self.channel_type,
            'channelNumber': self.channel_number,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceGetAnalogIORequest':
        return DeviceGetAnalogIORequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            channel_type=data.get('channelType'),  # type: ignore
            channel_number=data.get('channelNumber'),  # type: ignore
        )
