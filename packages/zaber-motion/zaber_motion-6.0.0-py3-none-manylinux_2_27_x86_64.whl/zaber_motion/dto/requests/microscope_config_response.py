# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..microscopy.microscope_config import MicroscopeConfig


@dataclass
class MicroscopeConfigResponse:

    config: MicroscopeConfig = field(default_factory=MicroscopeConfig.zero_values)

    @staticmethod
    def zero_values() -> 'MicroscopeConfigResponse':
        return MicroscopeConfigResponse(
            config=MicroscopeConfig.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'MicroscopeConfigResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return MicroscopeConfigResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'config': self.config.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MicroscopeConfigResponse':
        return MicroscopeConfigResponse(
            config=MicroscopeConfig.from_dict(data.get('config')),  # type: ignore
        )
