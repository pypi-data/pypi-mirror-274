# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class LockstepEnableRequest:

    interface_id: int = 0

    device: int = 0

    lockstep_group_id: int = 0

    axes: List[int] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'LockstepEnableRequest':
        return LockstepEnableRequest(
            interface_id=0,
            device=0,
            lockstep_group_id=0,
            axes=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepEnableRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepEnableRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'lockstepGroupId': self.lockstep_group_id,
            'axes': self.axes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepEnableRequest':
        return LockstepEnableRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            lockstep_group_id=data.get('lockstepGroupId'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
        )
