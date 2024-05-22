# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceDbFailedExceptionData:
    """
    Contains additional data for a DeviceDbFailedException.
    """

    code: str
    """
    Code describing type of the error.
    """

    @staticmethod
    def zero_values() -> 'DeviceDbFailedExceptionData':
        return DeviceDbFailedExceptionData(
            code="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceDbFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceDbFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'code': self.code,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceDbFailedExceptionData':
        return DeviceDbFailedExceptionData(
            code=data.get('code'),  # type: ignore
        )
