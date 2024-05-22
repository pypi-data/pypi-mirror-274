# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class CanSetStateAxisResponse:

    axis_number: int = 0

    error: Optional[str] = None

    @staticmethod
    def zero_values() -> 'CanSetStateAxisResponse':
        return CanSetStateAxisResponse(
            error=None,
            axis_number=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CanSetStateAxisResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CanSetStateAxisResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'error': self.error,
            'axisNumber': self.axis_number,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CanSetStateAxisResponse':
        return CanSetStateAxisResponse(
            error=data.get('error'),  # type: ignore
            axis_number=data.get('axisNumber'),  # type: ignore
        )
