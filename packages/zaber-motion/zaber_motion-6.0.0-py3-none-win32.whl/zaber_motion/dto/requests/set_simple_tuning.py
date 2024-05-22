# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.servo_tuning_paramset import ServoTuningParamset
from ..ascii.servo_tuning_param import ServoTuningParam


@dataclass
class SetSimpleTuning:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    paramset: ServoTuningParamset = next(first for first in ServoTuningParamset)

    load_mass: float = 0

    tuning_params: List[ServoTuningParam] = field(default_factory=list)

    carriage_mass: Optional[float] = None

    @staticmethod
    def zero_values() -> 'SetSimpleTuning':
        return SetSimpleTuning(
            interface_id=0,
            device=0,
            axis=0,
            paramset=next(first for first in ServoTuningParamset),
            carriage_mass=None,
            load_mass=0,
            tuning_params=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetSimpleTuning':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetSimpleTuning.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'paramset': self.paramset.value,
            'carriageMass': self.carriage_mass,
            'loadMass': self.load_mass,
            'tuningParams': [item.to_dict() for item in self.tuning_params],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetSimpleTuning':
        return SetSimpleTuning(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            paramset=ServoTuningParamset(data.get('paramset')),  # type: ignore
            carriage_mass=data.get('carriageMass'),  # type: ignore
            load_mass=data.get('loadMass'),  # type: ignore
            tuning_params=[ServoTuningParam.from_dict(item) for item in data.get('tuningParams')],  # type: ignore
        )
