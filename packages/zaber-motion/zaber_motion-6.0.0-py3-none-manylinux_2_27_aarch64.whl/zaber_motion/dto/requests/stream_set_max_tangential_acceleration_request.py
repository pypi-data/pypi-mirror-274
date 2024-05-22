# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class StreamSetMaxTangentialAccelerationRequest:

    interface_id: int = 0

    device: int = 0

    stream_id: int = 0

    pvt: bool = False

    max_tangential_acceleration: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'StreamSetMaxTangentialAccelerationRequest':
        return StreamSetMaxTangentialAccelerationRequest(
            interface_id=0,
            device=0,
            stream_id=0,
            pvt=False,
            max_tangential_acceleration=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamSetMaxTangentialAccelerationRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamSetMaxTangentialAccelerationRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'streamId': self.stream_id,
            'pvt': self.pvt,
            'maxTangentialAcceleration': self.max_tangential_acceleration,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamSetMaxTangentialAccelerationRequest':
        return StreamSetMaxTangentialAccelerationRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            stream_id=data.get('streamId'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
            max_tangential_acceleration=data.get('maxTangentialAcceleration'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
