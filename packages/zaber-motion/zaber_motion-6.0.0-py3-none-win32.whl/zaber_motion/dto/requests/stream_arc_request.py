# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .stream_segment_type import StreamSegmentType
from ..rotation_direction import RotationDirection
from ..measurement import Measurement


@dataclass
class StreamArcRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    type: StreamSegmentType = next(first for first in StreamSegmentType)

    rotation_direction: RotationDirection = next(first for first in RotationDirection)

    center_x: Measurement = field(default_factory=Measurement.zero_values)

    center_y: Measurement = field(default_factory=Measurement.zero_values)

    end_x: Measurement = field(default_factory=Measurement.zero_values)

    end_y: Measurement = field(default_factory=Measurement.zero_values)

    target_axes_indices: List[int] = field(default_factory=list)

    endpoint: List[Measurement] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'StreamArcRequest':
        return StreamArcRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            type=next(first for first in StreamSegmentType),
            rotation_direction=next(first for first in RotationDirection),
            center_x=Measurement.zero_values(),
            center_y=Measurement.zero_values(),
            end_x=Measurement.zero_values(),
            end_y=Measurement.zero_values(),
            target_axes_indices=[],
            endpoint=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamArcRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamArcRequest.from_dict(data)

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
            'rotationDirection': self.rotation_direction.value,
            'centerX': self.center_x.to_dict(),
            'centerY': self.center_y.to_dict(),
            'endX': self.end_x.to_dict(),
            'endY': self.end_y.to_dict(),
            'targetAxesIndices': self.target_axes_indices,
            'endpoint': [item.to_dict() for item in self.endpoint],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamArcRequest':
        return StreamArcRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            type=StreamSegmentType(data.get('type')),  # type: ignore
            rotation_direction=RotationDirection(data.get('rotationDirection')),  # type: ignore
            center_x=Measurement.from_dict(data.get('centerX')),  # type: ignore
            center_y=Measurement.from_dict(data.get('centerY')),  # type: ignore
            end_x=Measurement.from_dict(data.get('endX')),  # type: ignore
            end_y=Measurement.from_dict(data.get('endY')),  # type: ignore
            target_axes_indices=data.get('targetAxesIndices'),  # type: ignore
            endpoint=[Measurement.from_dict(item) for item in data.get('endpoint')],  # type: ignore
        )
