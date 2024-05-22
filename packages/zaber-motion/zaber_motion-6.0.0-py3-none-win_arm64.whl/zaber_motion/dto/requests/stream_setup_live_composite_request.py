# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.stream_axis_definition import StreamAxisDefinition
from ..ascii.pvt_axis_definition import PvtAxisDefinition


@dataclass
class StreamSetupLiveCompositeRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    axes: List[StreamAxisDefinition] = field(default_factory=list)

    pvt_axes: List[PvtAxisDefinition] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'StreamSetupLiveCompositeRequest':
        return StreamSetupLiveCompositeRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            axes=[],
            pvt_axes=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamSetupLiveCompositeRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamSetupLiveCompositeRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'streamId': self.stream_id,
            'pvt': self.pvt,
            'axes': [item.to_dict() for item in self.axes],
            'pvtAxes': [item.to_dict() for item in self.pvt_axes],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamSetupLiveCompositeRequest':
        return StreamSetupLiveCompositeRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            axes=[StreamAxisDefinition.from_dict(item) for item in data.get('axes')],  # type: ignore
            pvt_axes=[PvtAxisDefinition.from_dict(item) for item in data.get('pvtAxes')],  # type: ignore
        )
