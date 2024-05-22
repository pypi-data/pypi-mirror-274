# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.trigger_condition import TriggerCondition
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class TriggerFireWhenSettingRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    axis: int = 0

    setting: str = ""

    trigger_condition: TriggerCondition = next(first for first in TriggerCondition)

    value: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'TriggerFireWhenSettingRequest':
        return TriggerFireWhenSettingRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            axis=0,
            setting="",
            trigger_condition=next(first for first in TriggerCondition),
            value=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerFireWhenSettingRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerFireWhenSettingRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'axis': self.axis,
            'setting': self.setting,
            'triggerCondition': self.trigger_condition.value,
            'value': self.value,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerFireWhenSettingRequest':
        return TriggerFireWhenSettingRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            setting=data.get('setting'),  # type: ignore
            trigger_condition=TriggerCondition(data.get('triggerCondition')),  # type: ignore
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
