# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class FindDeviceRequest:

    interface_id: int = 0

    device_address: int = 0

    @staticmethod
    def zero_values() -> 'FindDeviceRequest':
        return FindDeviceRequest(
            interface_id=0,
            device_address=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'FindDeviceRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return FindDeviceRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'deviceAddress': self.device_address,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FindDeviceRequest':
        return FindDeviceRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device_address=data.get('deviceAddress'),  # type: ignore
        )
