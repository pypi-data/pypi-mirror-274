# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceCancelAllOutputsScheduleRequest:

    interface_id: int = 0

    device: int = 0

    analog: bool = False

    channels: List[bool] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DeviceCancelAllOutputsScheduleRequest':
        return DeviceCancelAllOutputsScheduleRequest(
            interface_id=0,
            device=0,
            analog=False,
            channels=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceCancelAllOutputsScheduleRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceCancelAllOutputsScheduleRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'analog': self.analog,
            'channels': self.channels,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceCancelAllOutputsScheduleRequest':
        return DeviceCancelAllOutputsScheduleRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            analog=data.get('analog'),  # type: ignore
            channels=data.get('channels'),  # type: ignore
        )
