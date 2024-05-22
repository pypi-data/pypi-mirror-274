# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .device_type import DeviceType


@dataclass
class DeviceDetectRequest:

    interface_id: int = 0

    identify_devices: bool = False

    type: DeviceType = next(first for first in DeviceType)

    @staticmethod
    def zero_values() -> 'DeviceDetectRequest':
        return DeviceDetectRequest(
            interface_id=0,
            identify_devices=False,
            type=next(first for first in DeviceType),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceDetectRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceDetectRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'identifyDevices': self.identify_devices,
            'type': self.type.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceDetectRequest':
        return DeviceDetectRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            identify_devices=data.get('identifyDevices'),  # type: ignore
            type=DeviceType(data.get('type')),  # type: ignore
        )
