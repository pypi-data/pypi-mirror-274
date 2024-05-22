# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class FirmwareVersion:
    """
    Class representing version of firmware in the controller.
    """

    major: int
    """
    Major version number.
    """

    minor: int
    """
    Minor version number.
    """

    build: int
    """
    Build version number.
    """

    @staticmethod
    def zero_values() -> 'FirmwareVersion':
        return FirmwareVersion(
            major=0,
            minor=0,
            build=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'FirmwareVersion':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return FirmwareVersion.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'major': self.major,
            'minor': self.minor,
            'build': self.build,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FirmwareVersion':
        return FirmwareVersion(
            major=data.get('major'),  # type: ignore
            minor=data.get('minor'),  # type: ignore
            build=data.get('build'),  # type: ignore
        )
