# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.unknown_response_event import UnknownResponseEvent


@dataclass
class UnknownResponseEventWrapper:

    interface_id: int = 0

    unknown_response: UnknownResponseEvent = field(default_factory=UnknownResponseEvent.zero_values)

    @staticmethod
    def zero_values() -> 'UnknownResponseEventWrapper':
        return UnknownResponseEventWrapper(
            interface_id=0,
            unknown_response=UnknownResponseEvent.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnknownResponseEventWrapper':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnknownResponseEventWrapper.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'unknownResponse': self.unknown_response.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnknownResponseEventWrapper':
        return UnknownResponseEventWrapper(
            interface_id=data.get('interfaceId'),  # type: ignore
            unknown_response=UnknownResponseEvent.from_dict(data.get('unknownResponse')),  # type: ignore
        )
