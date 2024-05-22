# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class StreamSetupLiveRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    axes: List[int] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'StreamSetupLiveRequest':
        return StreamSetupLiveRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            axes=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamSetupLiveRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamSetupLiveRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'streamId': self.stream_id,
            'pvt': self.pvt,
            'axes': self.axes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamSetupLiveRequest':
        return StreamSetupLiveRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
        )
