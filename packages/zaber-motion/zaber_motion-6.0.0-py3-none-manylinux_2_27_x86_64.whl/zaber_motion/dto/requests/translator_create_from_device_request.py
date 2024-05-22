# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..gcode.translator_config import TranslatorConfig


@dataclass
class TranslatorCreateFromDeviceRequest:

    interface_id: int = 0

    device: int = 0

    axes: List[int] = field(default_factory=list)

    config: Optional[TranslatorConfig] = None

    @staticmethod
    def zero_values() -> 'TranslatorCreateFromDeviceRequest':
        return TranslatorCreateFromDeviceRequest(
            interface_id=0,
            device=0,
            axes=[],
            config=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorCreateFromDeviceRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorCreateFromDeviceRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axes': self.axes,
            'config': self.config.to_dict() if self.config is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorCreateFromDeviceRequest':
        return TranslatorCreateFromDeviceRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
            config=TranslatorConfig.from_dict(data.get('config')) if data.get('config') is not None else None,  # type: ignore
        )
