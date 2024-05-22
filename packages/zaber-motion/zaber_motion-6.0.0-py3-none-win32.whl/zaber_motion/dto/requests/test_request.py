# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TestRequest:

    return_error: bool = False

    data_ping: str = ""

    return_error_with_data: bool = False

    @staticmethod
    def zero_values() -> 'TestRequest':
        return TestRequest(
            return_error=False,
            data_ping="",
            return_error_with_data=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TestRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TestRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'returnError': self.return_error,
            'dataPing': self.data_ping,
            'returnErrorWithData': self.return_error_with_data,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TestRequest':
        return TestRequest(
            return_error=data.get('returnError'),  # type: ignore
            data_ping=data.get('dataPing'),  # type: ignore
            return_error_with_data=data.get('returnErrorWithData'),  # type: ignore
        )
