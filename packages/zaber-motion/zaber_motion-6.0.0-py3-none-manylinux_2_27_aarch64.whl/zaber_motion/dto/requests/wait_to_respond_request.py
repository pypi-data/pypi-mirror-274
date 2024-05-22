# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class WaitToRespondRequest:

    interface_id: int = 0

    device: int = 0

    timeout: float = 0

    @staticmethod
    def zero_values() -> 'WaitToRespondRequest':
        return WaitToRespondRequest(
            interface_id=0,
            device=0,
            timeout=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'WaitToRespondRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return WaitToRespondRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'timeout': self.timeout,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WaitToRespondRequest':
        return WaitToRespondRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
        )
