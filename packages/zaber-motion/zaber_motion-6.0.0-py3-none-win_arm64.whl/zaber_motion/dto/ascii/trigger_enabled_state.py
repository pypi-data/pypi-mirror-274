# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TriggerEnabledState:
    """
    The enabled state of a single trigger.
    Returns whether the given trigger is enabled and the number of times it will fire.
    This is a subset of the complete state, and is faster to query.
    """

    enabled: bool
    """
    The enabled state for a trigger.
    """

    fires_remaining: int
    """
    The number of remaining fires for this trigger.
    A value of -1 indicates unlimited fires remaining.
    """

    @staticmethod
    def zero_values() -> 'TriggerEnabledState':
        return TriggerEnabledState(
            enabled=False,
            fires_remaining=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerEnabledState':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerEnabledState.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'enabled': self.enabled,
            'firesRemaining': self.fires_remaining,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerEnabledState':
        return TriggerEnabledState(
            enabled=data.get('enabled'),  # type: ignore
            fires_remaining=data.get('firesRemaining'),  # type: ignore
        )
