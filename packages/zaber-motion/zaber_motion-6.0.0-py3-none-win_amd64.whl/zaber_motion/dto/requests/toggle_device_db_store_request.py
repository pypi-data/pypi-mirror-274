# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class ToggleDeviceDbStoreRequest:

    toggle_on: bool = False

    store_location: str = ""

    @staticmethod
    def zero_values() -> 'ToggleDeviceDbStoreRequest':
        return ToggleDeviceDbStoreRequest(
            toggle_on=False,
            store_location="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ToggleDeviceDbStoreRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ToggleDeviceDbStoreRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'toggleOn': self.toggle_on,
            'storeLocation': self.store_location,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ToggleDeviceDbStoreRequest':
        return ToggleDeviceDbStoreRequest(
            toggle_on=data.get('toggleOn'),  # type: ignore
            store_location=data.get('storeLocation'),  # type: ignore
        )
