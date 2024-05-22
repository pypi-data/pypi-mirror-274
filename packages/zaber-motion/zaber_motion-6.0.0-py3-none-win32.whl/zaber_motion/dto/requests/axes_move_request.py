# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..measurement import Measurement


@dataclass
class AxesMoveRequest:

    interfaces: List[int] = field(default_factory=list)

    devices: List[int] = field(default_factory=list)

    axes: List[int] = field(default_factory=list)

    position: List[Measurement] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'AxesMoveRequest':
        return AxesMoveRequest(
            interfaces=[],
            devices=[],
            axes=[],
            position=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxesMoveRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxesMoveRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaces': self.interfaces,
            'devices': self.devices,
            'axes': self.axes,
            'position': [item.to_dict() for item in self.position],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxesMoveRequest':
        return AxesMoveRequest(
            interfaces=data.get('interfaces'),  # type: ignore
            devices=data.get('devices'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
            position=[Measurement.from_dict(item) for item in data.get('position')],  # type: ignore
        )
