# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class SetInterfaceChecksumEnabledRequest:

    interface_id: int = 0

    is_enabled: bool = False

    @staticmethod
    def zero_values() -> 'SetInterfaceChecksumEnabledRequest':
        return SetInterfaceChecksumEnabledRequest(
            interface_id=0,
            is_enabled=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetInterfaceChecksumEnabledRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetInterfaceChecksumEnabledRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'isEnabled': self.is_enabled,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetInterfaceChecksumEnabledRequest':
        return SetInterfaceChecksumEnabledRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            is_enabled=data.get('isEnabled'),  # type: ignore
        )
