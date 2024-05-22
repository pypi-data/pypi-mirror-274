# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class LockstepStopRequest:

    interface_id: int = 0

    device: int = 0

    lockstep_group_id: int = 0

    wait_until_idle: bool = False

    @staticmethod
    def zero_values() -> 'LockstepStopRequest':
        return LockstepStopRequest(
            interface_id=0,
            device=0,
            lockstep_group_id=0,
            wait_until_idle=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepStopRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepStopRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'lockstepGroupId': self.lockstep_group_id,
            'waitUntilIdle': self.wait_until_idle,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepStopRequest':
        return LockstepStopRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            lockstep_group_id=data.get('lockstepGroupId'),  # type: ignore
            wait_until_idle=data.get('waitUntilIdle'),  # type: ignore
        )
