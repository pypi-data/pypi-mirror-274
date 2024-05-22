# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.servo_tuning_paramset import ServoTuningParamset


@dataclass
class LoadParamset:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    to_paramset: ServoTuningParamset = next(first for first in ServoTuningParamset)

    from_paramset: ServoTuningParamset = next(first for first in ServoTuningParamset)

    @staticmethod
    def zero_values() -> 'LoadParamset':
        return LoadParamset(
            interface_id=0,
            device=0,
            axis=0,
            to_paramset=next(first for first in ServoTuningParamset),
            from_paramset=next(first for first in ServoTuningParamset),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LoadParamset':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LoadParamset.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'toParamset': self.to_paramset.value,
            'fromParamset': self.from_paramset.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LoadParamset':
        return LoadParamset(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            to_paramset=ServoTuningParamset(data.get('toParamset')),  # type: ignore
            from_paramset=ServoTuningParamset(data.get('fromParamset')),  # type: ignore
        )
