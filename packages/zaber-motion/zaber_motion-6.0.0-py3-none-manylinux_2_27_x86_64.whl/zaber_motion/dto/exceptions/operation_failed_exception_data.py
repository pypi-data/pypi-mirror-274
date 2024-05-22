# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class OperationFailedExceptionData:
    """
    Contains additional data for OperationFailedException.
    """

    warnings: List[str]
    """
    The full list of warnings.
    """

    reason: str
    """
    The reason for the Exception.
    """

    device: int
    """
    The address of the device that attempted the failed operation.
    """

    axis: int
    """
    The number of the axis that attempted the failed operation.
    """

    @staticmethod
    def zero_values() -> 'OperationFailedExceptionData':
        return OperationFailedExceptionData(
            warnings=[],
            reason="",
            device=0,
            axis=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OperationFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OperationFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'warnings': self.warnings,
            'reason': self.reason,
            'device': self.device,
            'axis': self.axis,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OperationFailedExceptionData':
        return OperationFailedExceptionData(
            warnings=data.get('warnings'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
        )
