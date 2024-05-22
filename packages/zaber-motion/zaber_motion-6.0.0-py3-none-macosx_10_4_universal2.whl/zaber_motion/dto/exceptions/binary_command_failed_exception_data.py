# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class BinaryCommandFailedExceptionData:
    """
    Contains additional data for BinaryCommandFailedException.
    """

    response_data: int
    """
    The response data.
    """

    @staticmethod
    def zero_values() -> 'BinaryCommandFailedExceptionData':
        return BinaryCommandFailedExceptionData(
            response_data=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryCommandFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryCommandFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'responseData': self.response_data,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryCommandFailedExceptionData':
        return BinaryCommandFailedExceptionData(
            response_data=data.get('responseData'),  # type: ignore
        )
