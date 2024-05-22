# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .stream_segment_type import StreamSegmentType
from ..measurement import Measurement


@dataclass
class StreamLineRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    type: StreamSegmentType = next(first for first in StreamSegmentType)

    endpoint: List[Measurement] = field(default_factory=list)

    target_axes_indices: List[int] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'StreamLineRequest':
        return StreamLineRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            type=next(first for first in StreamSegmentType),
            endpoint=[],
            target_axes_indices=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamLineRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamLineRequest.from_dict(data)

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
            'endpoint': [item.to_dict() for item in self.endpoint],
            'targetAxesIndices': self.target_axes_indices,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamLineRequest':
        return StreamLineRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            type=StreamSegmentType(data.get('type')),  # type: ignore
            endpoint=[Measurement.from_dict(item) for item in data.get('endpoint')],  # type: ignore
            target_axes_indices=data.get('targetAxesIndices'),  # type: ignore
        )
