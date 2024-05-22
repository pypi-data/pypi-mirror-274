# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .invalid_pvt_point import InvalidPvtPoint


@dataclass
class PvtExecutionExceptionData:
    """
    Contains additional data for PvtExecutionException.
    """

    error_flag: str
    """
    The error flag that caused the exception.
    """

    reason: str
    """
    The reason for the exception.
    """

    invalid_points: List[InvalidPvtPoint]
    """
    A list of points that cause the error (if applicable).
    """

    @staticmethod
    def zero_values() -> 'PvtExecutionExceptionData':
        return PvtExecutionExceptionData(
            error_flag="",
            reason="",
            invalid_points=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtExecutionExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtExecutionExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'errorFlag': self.error_flag,
            'reason': self.reason,
            'invalidPoints': [item.to_dict() for item in self.invalid_points],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtExecutionExceptionData':
        return PvtExecutionExceptionData(
            error_flag=data.get('errorFlag'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
            invalid_points=[InvalidPvtPoint.from_dict(item) for item in data.get('invalidPoints')],  # type: ignore
        )
