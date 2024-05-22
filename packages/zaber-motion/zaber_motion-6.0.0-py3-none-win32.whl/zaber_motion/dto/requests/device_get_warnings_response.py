# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceGetWarningsResponse:

    flags: List[str] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DeviceGetWarningsResponse':
        return DeviceGetWarningsResponse(
            flags=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceGetWarningsResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceGetWarningsResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'flags': self.flags,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceGetWarningsResponse':
        return DeviceGetWarningsResponse(
            flags=data.get('flags'),  # type: ignore
        )
