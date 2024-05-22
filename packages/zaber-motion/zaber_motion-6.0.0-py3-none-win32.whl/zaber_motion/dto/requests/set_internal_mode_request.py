# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class SetInternalModeRequest:

    mode: bool = False

    @staticmethod
    def zero_values() -> 'SetInternalModeRequest':
        return SetInternalModeRequest(
            mode=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetInternalModeRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetInternalModeRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'mode': self.mode,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetInternalModeRequest':
        return SetInternalModeRequest(
            mode=data.get('mode'),  # type: ignore
        )
