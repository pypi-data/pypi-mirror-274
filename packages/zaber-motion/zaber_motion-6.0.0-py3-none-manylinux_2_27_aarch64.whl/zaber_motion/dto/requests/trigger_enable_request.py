# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TriggerEnableRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    count: int = 0

    @staticmethod
    def zero_values() -> 'TriggerEnableRequest':
        return TriggerEnableRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            count=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerEnableRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerEnableRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'count': self.count,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerEnableRequest':
        return TriggerEnableRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            count=data.get('count'),  # type: ignore
        )
