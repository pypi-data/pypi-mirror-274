# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceAddressConflictExceptionData:
    """
    Contains additional data for DeviceAddressConflictException.
    """

    device_addresses: List[int]
    """
    The full list of detected device addresses.
    """

    @staticmethod
    def zero_values() -> 'DeviceAddressConflictExceptionData':
        return DeviceAddressConflictExceptionData(
            device_addresses=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceAddressConflictExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceAddressConflictExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceAddresses': self.device_addresses,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceAddressConflictExceptionData':
        return DeviceAddressConflictExceptionData(
            device_addresses=data.get('deviceAddresses'),  # type: ignore
        )
