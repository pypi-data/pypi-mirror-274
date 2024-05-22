# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .axis_definition import AxisDefinition
from ..measurement import Measurement


@dataclass
class DeviceDefinition:
    """
    Holds information about device and its axes for purpose of a translator.
    """

    device_id: int
    """
    Device ID of the controller.
    Can be obtained from device settings.
    """

    axes: List[AxisDefinition]
    """
    Applicable axes of the device.
    """

    max_speed: Measurement
    """
    The smallest of each axis' maxspeed setting value.
    This value becomes the traverse rate of the translator.
    """

    @staticmethod
    def zero_values() -> 'DeviceDefinition':
        return DeviceDefinition(
            device_id=0,
            axes=[],
            max_speed=Measurement.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceDefinition':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceDefinition.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceId': self.device_id,
            'axes': [item.to_dict() for item in self.axes],
            'maxSpeed': self.max_speed.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceDefinition':
        return DeviceDefinition(
            device_id=data.get('deviceId'),  # type: ignore
            axes=[AxisDefinition.from_dict(item) for item in data.get('axes')],  # type: ignore
            max_speed=Measurement.from_dict(data.get('maxSpeed')),  # type: ignore
        )
