# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class CustomInterfaceWriteRequest:

    transport_id: int = 0

    message: str = ""

    @staticmethod
    def zero_values() -> 'CustomInterfaceWriteRequest':
        return CustomInterfaceWriteRequest(
            transport_id=0,
            message="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CustomInterfaceWriteRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CustomInterfaceWriteRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'transportId': self.transport_id,
            'message': self.message,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CustomInterfaceWriteRequest':
        return CustomInterfaceWriteRequest(
            transport_id=data.get('transportId'),  # type: ignore
            message=data.get('message'),  # type: ignore
        )
