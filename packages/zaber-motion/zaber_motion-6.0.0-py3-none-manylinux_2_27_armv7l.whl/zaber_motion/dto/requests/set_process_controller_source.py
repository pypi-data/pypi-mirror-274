# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..product.process_controller_source import ProcessControllerSource


@dataclass
class SetProcessControllerSource:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    source: ProcessControllerSource = field(default_factory=ProcessControllerSource.zero_values)

    @staticmethod
    def zero_values() -> 'SetProcessControllerSource':
        return SetProcessControllerSource(
            interface_id=0,
            device=0,
            axis=0,
            source=ProcessControllerSource.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetProcessControllerSource':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetProcessControllerSource.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'source': self.source.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetProcessControllerSource':
        return SetProcessControllerSource(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            source=ProcessControllerSource.from_dict(data.get('source')),  # type: ignore
        )
