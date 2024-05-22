# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.alert_event import AlertEvent


@dataclass
class AlertEventWrapper:

    interface_id: int = 0

    alert: AlertEvent = field(default_factory=AlertEvent.zero_values)

    @staticmethod
    def zero_values() -> 'AlertEventWrapper':
        return AlertEventWrapper(
            interface_id=0,
            alert=AlertEvent.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AlertEventWrapper':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AlertEventWrapper.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'alert': self.alert.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AlertEventWrapper':
        return AlertEventWrapper(
            interface_id=data.get('interfaceId'),  # type: ignore
            alert=AlertEvent.from_dict(data.get('alert')),  # type: ignore
        )
