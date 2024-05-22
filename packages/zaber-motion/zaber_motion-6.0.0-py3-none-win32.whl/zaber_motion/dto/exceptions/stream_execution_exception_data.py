# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class StreamExecutionExceptionData:
    """
    Contains additional data for StreamExecutionException.
    """

    error_flag: str
    """
    The error flag that caused the exception.
    """

    reason: str
    """
    The reason for the exception.
    """

    @staticmethod
    def zero_values() -> 'StreamExecutionExceptionData':
        return StreamExecutionExceptionData(
            error_flag="",
            reason="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamExecutionExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamExecutionExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'errorFlag': self.error_flag,
            'reason': self.reason,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamExecutionExceptionData':
        return StreamExecutionExceptionData(
            error_flag=data.get('errorFlag'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
        )
