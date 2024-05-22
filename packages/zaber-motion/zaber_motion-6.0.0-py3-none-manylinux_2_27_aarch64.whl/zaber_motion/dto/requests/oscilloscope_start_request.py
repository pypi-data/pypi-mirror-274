# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class OscilloscopeStartRequest:

    interface_id: int = 0

    device: int = 0

    capture_length: int = 0

    @staticmethod
    def zero_values() -> 'OscilloscopeStartRequest':
        return OscilloscopeStartRequest(
            interface_id=0,
            device=0,
            capture_length=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OscilloscopeStartRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OscilloscopeStartRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'captureLength': self.capture_length,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OscilloscopeStartRequest':
        return OscilloscopeStartRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            capture_length=data.get('captureLength'),  # type: ignore
        )
