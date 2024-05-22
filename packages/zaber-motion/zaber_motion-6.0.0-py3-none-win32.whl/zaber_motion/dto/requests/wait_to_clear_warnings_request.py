# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class WaitToClearWarningsRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    timeout: float = 0

    warning_flags: List[str] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'WaitToClearWarningsRequest':
        return WaitToClearWarningsRequest(
            interface_id=0,
            device=0,
            axis=0,
            timeout=0,
            warning_flags=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'WaitToClearWarningsRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return WaitToClearWarningsRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'timeout': self.timeout,
            'warningFlags': self.warning_flags,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'WaitToClearWarningsRequest':
        return WaitToClearWarningsRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
            warning_flags=data.get('warningFlags'),  # type: ignore
        )
