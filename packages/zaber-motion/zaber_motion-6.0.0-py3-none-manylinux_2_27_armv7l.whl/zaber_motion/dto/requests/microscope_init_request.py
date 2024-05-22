# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..microscopy.microscope_config import MicroscopeConfig


@dataclass
class MicroscopeInitRequest:

    interface_id: int = 0

    config: MicroscopeConfig = field(default_factory=MicroscopeConfig.zero_values)

    force: bool = False

    @staticmethod
    def zero_values() -> 'MicroscopeInitRequest':
        return MicroscopeInitRequest(
            interface_id=0,
            config=MicroscopeConfig.zero_values(),
            force=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'MicroscopeInitRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return MicroscopeInitRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'config': self.config.to_dict(),
            'force': self.force,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MicroscopeInitRequest':
        return MicroscopeInitRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            config=MicroscopeConfig.from_dict(data.get('config')),  # type: ignore
            force=data.get('force'),  # type: ignore
        )
