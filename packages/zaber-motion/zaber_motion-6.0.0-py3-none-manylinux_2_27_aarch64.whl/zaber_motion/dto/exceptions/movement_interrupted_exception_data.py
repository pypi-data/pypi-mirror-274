# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class MovementInterruptedExceptionData:
    """
    Contains additional data for MovementInterruptedException.
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
    The address of the device that caused the interruption.
    """

    axis: int
    """
    The number of the axis that caused the interruption.
    """

    @staticmethod
    def zero_values() -> 'MovementInterruptedExceptionData':
        return MovementInterruptedExceptionData(
            warnings=[],
            reason="",
            device=0,
            axis=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'MovementInterruptedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return MovementInterruptedExceptionData.from_dict(data)

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
    def from_dict(data: Dict[str, Any]) -> 'MovementInterruptedExceptionData':
        return MovementInterruptedExceptionData(
            warnings=data.get('warnings'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
        )
