# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class AxisToStringRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    type_override: str = ""

    @staticmethod
    def zero_values() -> 'AxisToStringRequest':
        return AxisToStringRequest(
            interface_id=0,
            device=0,
            axis=0,
            type_override="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxisToStringRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxisToStringRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'typeOverride': self.type_override,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxisToStringRequest':
        return AxisToStringRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            type_override=data.get('typeOverride'),  # type: ignore
        )
