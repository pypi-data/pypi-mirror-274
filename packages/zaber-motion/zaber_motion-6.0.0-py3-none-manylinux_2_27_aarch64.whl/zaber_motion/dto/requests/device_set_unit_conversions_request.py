# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.conversion_factor import ConversionFactor


@dataclass
class DeviceSetUnitConversionsRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    key: str = ""

    conversions: List[ConversionFactor] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DeviceSetUnitConversionsRequest':
        return DeviceSetUnitConversionsRequest(
            interface_id=0,
            device=0,
            axis=0,
            key="",
            conversions=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceSetUnitConversionsRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceSetUnitConversionsRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'key': self.key,
            'conversions': [item.to_dict() for item in self.conversions],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceSetUnitConversionsRequest':
        return DeviceSetUnitConversionsRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            key=data.get('key'),  # type: ignore
            conversions=[ConversionFactor.from_dict(item) for item in data.get('conversions')],  # type: ignore
        )
