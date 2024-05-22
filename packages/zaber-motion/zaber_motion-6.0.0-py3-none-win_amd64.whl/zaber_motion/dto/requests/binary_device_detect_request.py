# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class BinaryDeviceDetectRequest:

    interface_id: int = 0

    identify_devices: bool = False

    @staticmethod
    def zero_values() -> 'BinaryDeviceDetectRequest':
        return BinaryDeviceDetectRequest(
            interface_id=0,
            identify_devices=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryDeviceDetectRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryDeviceDetectRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'identifyDevices': self.identify_devices,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryDeviceDetectRequest':
        return BinaryDeviceDetectRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            identify_devices=data.get('identifyDevices'),  # type: ignore
        )
