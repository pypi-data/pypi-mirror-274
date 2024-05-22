# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TriggerFireWhenRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    condition: str = ""

    @staticmethod
    def zero_values() -> 'TriggerFireWhenRequest':
        return TriggerFireWhenRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            condition="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerFireWhenRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerFireWhenRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'condition': self.condition,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerFireWhenRequest':
        return TriggerFireWhenRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            condition=data.get('condition'),  # type: ignore
        )
