# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .stream_segment_type import StreamSegmentType
from ..measurement import Measurement


@dataclass
class PvtPointRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    type: StreamSegmentType = next(first for first in StreamSegmentType)

    positions: List[Measurement] = field(default_factory=list)

    velocities: List[Optional[Measurement]] = field(default_factory=list)

    time: Measurement = field(default_factory=Measurement.zero_values)

    @staticmethod
    def zero_values() -> 'PvtPointRequest':
        return PvtPointRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            type=next(first for first in StreamSegmentType),
            positions=[],
            velocities=[],
            time=Measurement.zero_values(),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtPointRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtPointRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'streamId': self.stream_id,
            'pvt': self.pvt,
            'type': self.type.value,
            'positions': [item.to_dict() for item in self.positions],
            'velocities': [item.to_dict() if item is not None else None for item in self.velocities],
            'time': self.time.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtPointRequest':
        return PvtPointRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            type=StreamSegmentType(data.get('type')),  # type: ignore
            positions=[Measurement.from_dict(item) for item in data.get('positions')],  # type: ignore
            velocities=[Measurement.from_dict(item) if item is not None else None for item in data.get('velocities')],  # type: ignore
            time=Measurement.from_dict(data.get('time')),  # type: ignore
        )
