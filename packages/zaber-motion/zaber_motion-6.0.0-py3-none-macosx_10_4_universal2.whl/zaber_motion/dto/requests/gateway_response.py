# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .response_type import ResponseType
from .errors import Errors


@dataclass
class GatewayResponse:

    response: ResponseType = next(first for first in ResponseType)

    error_type: Errors = next(first for first in Errors)

    error_message: str = ""

    @staticmethod
    def zero_values() -> 'GatewayResponse':
        return GatewayResponse(
            response=next(first for first in ResponseType),
            error_type=next(first for first in Errors),
            error_message="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GatewayResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GatewayResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'response': self.response.value,
            'errorType': self.error_type.value,
            'errorMessage': self.error_message,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GatewayResponse':
        return GatewayResponse(
            response=ResponseType(data.get('response')),  # type: ignore
            error_type=Errors(data.get('errorType')),  # type: ignore
            error_message=data.get('errorMessage'),  # type: ignore
        )
