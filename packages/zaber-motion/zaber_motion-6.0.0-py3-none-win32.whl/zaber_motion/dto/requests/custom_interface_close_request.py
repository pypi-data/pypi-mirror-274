# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class CustomInterfaceCloseRequest:

    transport_id: int = 0

    error_message: str = ""

    @staticmethod
    def zero_values() -> 'CustomInterfaceCloseRequest':
        return CustomInterfaceCloseRequest(
            transport_id=0,
            error_message="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CustomInterfaceCloseRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CustomInterfaceCloseRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'transportId': self.transport_id,
            'errorMessage': self.error_message,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CustomInterfaceCloseRequest':
        return CustomInterfaceCloseRequest(
            transport_id=data.get('transportId'),  # type: ignore
            error_message=data.get('errorMessage'),  # type: ignore
        )
