# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .servo_tuning_param import ServoTuningParam


@dataclass
class SimpleTuning:
    """
    The masses and parameters last used by simple tuning.
    """

    is_used: bool
    """
    Whether the tuning returned is currently in use by this paramset,
    or if it has been overwritten by a later change.
    """

    load_mass: float
    """
    The mass of the load in kg, excluding the mass of the carriage.
    """

    tuning_params: List[ServoTuningParam]
    """
    The parameters used by simple tuning.
    """

    carriage_mass: Optional[float] = None
    """
    The mass of the carriage in kg.
    """

    @staticmethod
    def zero_values() -> 'SimpleTuning':
        return SimpleTuning(
            is_used=False,
            carriage_mass=None,
            load_mass=0,
            tuning_params=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SimpleTuning':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SimpleTuning.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'isUsed': self.is_used,
            'carriageMass': self.carriage_mass,
            'loadMass': self.load_mass,
            'tuningParams': [item.to_dict() for item in self.tuning_params],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SimpleTuning':
        return SimpleTuning(
            is_used=data.get('isUsed'),  # type: ignore
            carriage_mass=data.get('carriageMass'),  # type: ignore
            load_mass=data.get('loadMass'),  # type: ignore
            tuning_params=[ServoTuningParam.from_dict(item) for item in data.get('tuningParams')],  # type: ignore
        )
