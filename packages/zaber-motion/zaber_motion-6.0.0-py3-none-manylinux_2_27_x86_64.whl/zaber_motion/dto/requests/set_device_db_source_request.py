# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..device_db_source_type import DeviceDbSourceType


@dataclass
class SetDeviceDbSourceRequest:

    source_type: DeviceDbSourceType = next(first for first in DeviceDbSourceType)

    url_or_file_path: str = ""

    @staticmethod
    def zero_values() -> 'SetDeviceDbSourceRequest':
        return SetDeviceDbSourceRequest(
            source_type=next(first for first in DeviceDbSourceType),
            url_or_file_path="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetDeviceDbSourceRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetDeviceDbSourceRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sourceType': self.source_type.value,
            'urlOrFilePath': self.url_or_file_path,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetDeviceDbSourceRequest':
        return SetDeviceDbSourceRequest(
            source_type=DeviceDbSourceType(data.get('sourceType')),  # type: ignore
            url_or_file_path=data.get('urlOrFilePath'),  # type: ignore
        )
