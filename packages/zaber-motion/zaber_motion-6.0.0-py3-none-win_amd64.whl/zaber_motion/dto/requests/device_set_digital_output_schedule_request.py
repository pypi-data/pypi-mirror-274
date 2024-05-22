# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.digital_output_action import DigitalOutputAction
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class DeviceSetDigitalOutputScheduleRequest:

    interface_id: int = 0

    device: int = 0

    channel_number: int = 0

    value: DigitalOutputAction = next(first for first in DigitalOutputAction)

    future_value: DigitalOutputAction = next(first for first in DigitalOutputAction)

    delay: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'DeviceSetDigitalOutputScheduleRequest':
        return DeviceSetDigitalOutputScheduleRequest(
            interface_id=0,
            device=0,
            channel_number=0,
            value=next(first for first in DigitalOutputAction),
            future_value=next(first for first in DigitalOutputAction),
            delay=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceSetDigitalOutputScheduleRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceSetDigitalOutputScheduleRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'channelNumber': self.channel_number,
            'value': self.value.value,
            'futureValue': self.future_value.value,
            'delay': self.delay,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceSetDigitalOutputScheduleRequest':
        return DeviceSetDigitalOutputScheduleRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            channel_number=data.get('channelNumber'),  # type: ignore
            value=DigitalOutputAction(data.get('value')),  # type: ignore
            future_value=DigitalOutputAction(data.get('futureValue')),  # type: ignore
            delay=data.get('delay'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
