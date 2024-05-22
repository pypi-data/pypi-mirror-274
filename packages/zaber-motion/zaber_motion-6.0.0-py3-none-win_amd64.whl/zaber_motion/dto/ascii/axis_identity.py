# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .axis_type import AxisType


@dataclass
class AxisIdentity:
    """
    Representation of data gathered during axis identification.
    """

    peripheral_id: int
    """
    Unique ID of the peripheral hardware.
    """

    peripheral_name: str
    """
    Name of the peripheral.
    """

    peripheral_serial_number: int
    """
    Serial number of the peripheral, or 0 when not applicable.
    """

    is_peripheral: bool
    """
    Indicates whether the axis is a peripheral or part of an integrated device.
    """

    axis_type: AxisType
    """
    Determines the type of an axis and units it accepts.
    """

    is_modified: bool
    """
    The peripheral has hardware modifications.
    """

    @staticmethod
    def zero_values() -> 'AxisIdentity':
        return AxisIdentity(
            peripheral_id=0,
            peripheral_name="",
            peripheral_serial_number=0,
            is_peripheral=False,
            axis_type=next(first for first in AxisType),
            is_modified=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxisIdentity':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxisIdentity.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'peripheralId': self.peripheral_id,
            'peripheralName': self.peripheral_name,
            'peripheralSerialNumber': self.peripheral_serial_number,
            'isPeripheral': self.is_peripheral,
            'axisType': self.axis_type.value,
            'isModified': self.is_modified,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxisIdentity':
        return AxisIdentity(
            peripheral_id=data.get('peripheralId'),  # type: ignore
            peripheral_name=data.get('peripheralName'),  # type: ignore
            peripheral_serial_number=data.get('peripheralSerialNumber'),  # type: ignore
            is_peripheral=data.get('isPeripheral'),  # type: ignore
            axis_type=AxisType(data.get('axisType')),  # type: ignore
            is_modified=data.get('isModified'),  # type: ignore
        )
