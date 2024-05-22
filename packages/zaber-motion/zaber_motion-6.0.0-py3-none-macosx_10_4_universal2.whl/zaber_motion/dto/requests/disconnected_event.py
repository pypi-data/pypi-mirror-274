# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .errors import Errors


@dataclass
class DisconnectedEvent:
    """
    Event that is sent when a connection is lost.
    """

    interface_id: int = 0
    """
    The id of the interface that was disconnected.
    """

    error_type: Errors = next(first for first in Errors)
    """
    The type of error that caused the disconnection.
    """

    error_message: str = ""
    """
    The message describing the error.
    """

    @staticmethod
    def zero_values() -> 'DisconnectedEvent':
        return DisconnectedEvent(
            interface_id=0,
            error_type=next(first for first in Errors),
            error_message="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DisconnectedEvent':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DisconnectedEvent.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'errorType': self.error_type.value,
            'errorMessage': self.error_message,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DisconnectedEvent':
        return DisconnectedEvent(
            interface_id=data.get('interfaceId'),  # type: ignore
            error_type=Errors(data.get('errorType')),  # type: ignore
            error_message=data.get('errorMessage'),  # type: ignore
        )
