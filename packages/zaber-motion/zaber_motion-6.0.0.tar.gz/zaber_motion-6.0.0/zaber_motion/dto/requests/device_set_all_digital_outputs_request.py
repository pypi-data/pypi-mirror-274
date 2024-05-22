# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.digital_output_action import DigitalOutputAction


@dataclass
class DeviceSetAllDigitalOutputsRequest:

    interface_id: int = 0

    device: int = 0

    values: List[DigitalOutputAction] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DeviceSetAllDigitalOutputsRequest':
        return DeviceSetAllDigitalOutputsRequest(
            interface_id=0,
            device=0,
            values=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceSetAllDigitalOutputsRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceSetAllDigitalOutputsRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'values': [item.value for item in self.values],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceSetAllDigitalOutputsRequest':
        return DeviceSetAllDigitalOutputsRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            values=[DigitalOutputAction(item) for item in data.get('values')],  # type: ignore
        )
