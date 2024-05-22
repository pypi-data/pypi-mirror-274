# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class PvtMovementFailedExceptionData:
    """
    Contains additional data for PvtMovementFailedException.
    """

    warnings: List[str]
    """
    The full list of warnings.
    """

    reason: str
    """
    The reason for the Exception.
    """

    @staticmethod
    def zero_values() -> 'PvtMovementFailedExceptionData':
        return PvtMovementFailedExceptionData(
            warnings=[],
            reason="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtMovementFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtMovementFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'warnings': self.warnings,
            'reason': self.reason,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtMovementFailedExceptionData':
        return PvtMovementFailedExceptionData(
            warnings=data.get('warnings'),  # type: ignore
            reason=data.get('reason'),  # type: ignore
        )
