# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.trigger_action import TriggerAction


@dataclass
class TriggerClearActionRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    action: TriggerAction = next(first for first in TriggerAction)

    @staticmethod
    def zero_values() -> 'TriggerClearActionRequest':
        return TriggerClearActionRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            action=next(first for first in TriggerAction),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerClearActionRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerClearActionRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'action': self.action.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerClearActionRequest':
        return TriggerClearActionRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            action=TriggerAction(data.get('action')),  # type: ignore
        )
