# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class DeviceSetAllAnalogOutputsScheduleRequest:

    interface_id: int = 0

    device: int = 0

    values: List[float] = field(default_factory=list)

    future_values: List[float] = field(default_factory=list)

    delay: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'DeviceSetAllAnalogOutputsScheduleRequest':
        return DeviceSetAllAnalogOutputsScheduleRequest(
            interface_id=0,
            device=0,
            values=[],
            future_values=[],
            delay=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceSetAllAnalogOutputsScheduleRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceSetAllAnalogOutputsScheduleRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'values': self.values,
            'futureValues': self.future_values,
            'delay': self.delay,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceSetAllAnalogOutputsScheduleRequest':
        return DeviceSetAllAnalogOutputsScheduleRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            values=data.get('values'),  # type: ignore
            future_values=data.get('futureValues'),  # type: ignore
            delay=data.get('delay'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
