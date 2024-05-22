# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class InvalidResponseExceptionData:
    """
    Contains additional data for InvalidResponseException.
    """

    response: str
    """
    The response data.
    """

    @staticmethod
    def zero_values() -> 'InvalidResponseExceptionData':
        return InvalidResponseExceptionData(
            response="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'InvalidResponseExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return InvalidResponseExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'response': self.response,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'InvalidResponseExceptionData':
        return InvalidResponseExceptionData(
            response=data.get('response'),  # type: ignore
        )
