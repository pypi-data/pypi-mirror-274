# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceGetAllAnalogIORequest:

    interface_id: int = 0

    device: int = 0

    channel_type: str = ""

    @staticmethod
    def zero_values() -> 'DeviceGetAllAnalogIORequest':
        return DeviceGetAllAnalogIORequest(
            interface_id=0,
            device=0,
            channel_type="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceGetAllAnalogIORequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceGetAllAnalogIORequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'channelType': self.channel_type,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceGetAllAnalogIORequest':
        return DeviceGetAllAnalogIORequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            channel_type=data.get('channelType'),  # type: ignore
        )
