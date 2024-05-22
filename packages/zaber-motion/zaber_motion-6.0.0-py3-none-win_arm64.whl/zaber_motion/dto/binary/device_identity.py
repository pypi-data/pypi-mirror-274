# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..firmware_version import FirmwareVersion
from .device_type import DeviceType


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
    Requires at least Firmware 6.15 for devices or 6.24 for peripherals.
    """

    name: str
    """
    Name of the product.
    """

    firmware_version: FirmwareVersion
    """
    Version of the firmware.
    """

    is_peripheral: bool
    """
    Indicates whether the device is a peripheral or part of an integrated device.
    """

    peripheral_id: int
    """
    Unique ID of the peripheral hardware.
    """

    peripheral_name: str
    """
    Name of the peripheral hardware.
    """

    device_type: DeviceType
    """
    Determines the type of an device and units it accepts.
    """

    @staticmethod
    def zero_values() -> 'DeviceIdentity':
        return DeviceIdentity(
            device_id=0,
            serial_number=0,
            name="",
            firmware_version=FirmwareVersion.zero_values(),
            is_peripheral=False,
            peripheral_id=0,
            peripheral_name="",
            device_type=next(first for first in DeviceType),
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
            'firmwareVersion': self.firmware_version.to_dict(),
            'isPeripheral': self.is_peripheral,
            'peripheralId': self.peripheral_id,
            'peripheralName': self.peripheral_name,
            'deviceType': self.device_type.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceIdentity':
        return DeviceIdentity(
            device_id=data.get('deviceId'),  # type: ignore
            serial_number=data.get('serialNumber'),  # type: ignore
            name=data.get('name'),  # type: ignore
            firmware_version=FirmwareVersion.from_dict(data.get('firmwareVersion')),  # type: ignore
            is_peripheral=data.get('isPeripheral'),  # type: ignore
            peripheral_id=data.get('peripheralId'),  # type: ignore
            peripheral_name=data.get('peripheralName'),  # type: ignore
            device_type=DeviceType(data.get('deviceType')),  # type: ignore
        )
