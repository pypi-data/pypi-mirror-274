# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.servo_tuning_paramset import ServoTuningParamset


@dataclass
class SetServoTuningPIDRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    paramset: ServoTuningParamset = next(first for first in ServoTuningParamset)

    p: float = 0

    i: float = 0

    d: float = 0

    fc: float = 0

    @staticmethod
    def zero_values() -> 'SetServoTuningPIDRequest':
        return SetServoTuningPIDRequest(
            interface_id=0,
            device=0,
            axis=0,
            paramset=next(first for first in ServoTuningParamset),
            p=0,
            i=0,
            d=0,
            fc=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetServoTuningPIDRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetServoTuningPIDRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'paramset': self.paramset.value,
            'p': self.p,
            'i': self.i,
            'd': self.d,
            'fc': self.fc,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetServoTuningPIDRequest':
        return SetServoTuningPIDRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            paramset=ServoTuningParamset(data.get('paramset')),  # type: ignore
            p=data.get('p'),  # type: ignore
            i=data.get('i'),  # type: ignore
            d=data.get('d'),  # type: ignore
            fc=data.get('fc'),  # type: ignore
        )
