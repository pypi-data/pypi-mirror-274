# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.trigger_state import TriggerState


@dataclass
class TriggerStates:

    states: List[TriggerState] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'TriggerStates':
        return TriggerStates(
            states=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerStates':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerStates.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'states': [item.to_dict() for item in self.states],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerStates':
        return TriggerStates(
            states=[TriggerState.from_dict(item) for item in data.get('states')],  # type: ignore
        )
