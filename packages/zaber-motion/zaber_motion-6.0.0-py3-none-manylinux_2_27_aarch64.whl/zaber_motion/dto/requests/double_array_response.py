# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DoubleArrayResponse:

    values: List[float] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DoubleArrayResponse':
        return DoubleArrayResponse(
            values=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DoubleArrayResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DoubleArrayResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'values': self.values,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DoubleArrayResponse':
        return DoubleArrayResponse(
            values=data.get('values'),  # type: ignore
        )
