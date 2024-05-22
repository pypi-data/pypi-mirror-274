# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.trigger_action import TriggerAction
from ..ascii.trigger_operation import TriggerOperation


@dataclass
class TriggerOnFireSetToSettingRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    action: TriggerAction = next(first for first in TriggerAction)

    axis: int = 0

    setting: str = ""

    operation: TriggerOperation = next(first for first in TriggerOperation)

    from_axis: int = 0

    from_setting: str = ""

    @staticmethod
    def zero_values() -> 'TriggerOnFireSetToSettingRequest':
        return TriggerOnFireSetToSettingRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            action=next(first for first in TriggerAction),
            axis=0,
            setting="",
            operation=next(first for first in TriggerOperation),
            from_axis=0,
            from_setting="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerOnFireSetToSettingRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerOnFireSetToSettingRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'action': self.action.value,
            'axis': self.axis,
            'setting': self.setting,
            'operation': self.operation.value,
            'fromAxis': self.from_axis,
            'fromSetting': self.from_setting,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerOnFireSetToSettingRequest':
        return TriggerOnFireSetToSettingRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            action=TriggerAction(data.get('action')),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            setting=data.get('setting'),  # type: ignore
            operation=TriggerOperation(data.get('operation')),  # type: ignore
            from_axis=data.get('fromAxis'),  # type: ignore
            from_setting=data.get('fromSetting'),  # type: ignore
        )
