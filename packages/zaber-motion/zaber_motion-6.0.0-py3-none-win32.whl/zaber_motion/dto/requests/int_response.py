# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class IntResponse:

    value: int = 0

    @staticmethod
    def zero_values() -> 'IntResponse':
        return IntResponse(
            value=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'IntResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return IntResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'value': self.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'IntResponse':
        return IntResponse(
            value=data.get('value'),  # type: ignore
        )
