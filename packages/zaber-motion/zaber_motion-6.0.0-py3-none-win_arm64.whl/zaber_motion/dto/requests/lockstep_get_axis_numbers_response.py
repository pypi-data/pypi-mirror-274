# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class LockstepGetAxisNumbersResponse:

    axes: List[int] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'LockstepGetAxisNumbersResponse':
        return LockstepGetAxisNumbersResponse(
            axes=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepGetAxisNumbersResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepGetAxisNumbersResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axes': self.axes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepGetAxisNumbersResponse':
        return LockstepGetAxisNumbersResponse(
            axes=data.get('axes'),  # type: ignore
        )
