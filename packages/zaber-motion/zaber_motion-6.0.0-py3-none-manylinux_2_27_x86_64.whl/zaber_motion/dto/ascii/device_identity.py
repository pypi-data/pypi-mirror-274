# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..firmware_version import FirmwareVersion


@dataclass
class DeviceIdentity:
    """
    Representation of data gathered during device identification.
    """

    device_id: int
    """
    Unique ID of the device hardware.
    """

    serial_number: int
    """
    Serial number of the device.
    """

    name: str
    """
    Name of the product.
    """

    axis_count: int
    """
    Number of axes this device has.
    """

    firmware_version: FirmwareVersion
    """
    Version of the firmware.
    """

    is_modified: bool
    """
    The device has hardware modifications.
    """

    is_integrated: bool
    """
    The device is an integrated product.
    """

    @staticmethod
    def zero_values() -> 'DeviceIdentity':
        return DeviceIdentity(
            device_id=0,
            serial_number=0,
            name="",
            axis_count=0,
            firmware_version=FirmwareVersion.zero_values(),
            is_modified=False,
            is_integrated=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceIdentity':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceIdentity.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceId': self.device_id,
            'serialNumber': self.serial_number,
            'name': self.name,
            'axisCount': self.axis_count,
            'firmwareVersion': self.firmware_version.to_dict(),
            'isModified': self.is_modified,
            'isIntegrated': self.is_integrated,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceIdentity':
        return DeviceIdentity(
            device_id=data.get('deviceId'),  # type: ignore
            serial_number=data.get('serialNumber'),  # type: ignore
            name=data.get('name'),  # type: ignore
            axis_count=data.get('axisCount'),  # type: ignore
            firmware_version=FirmwareVersion.from_dict(data.get('firmwareVersion')),  # type: ignore
            is_modified=data.get('isModified'),  # type: ignore
            is_integrated=data.get('isIntegrated'),  # type: ignore
        )
