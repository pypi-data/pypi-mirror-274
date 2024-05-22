# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.servo_tuning_paramset import ServoTuningParamset


@dataclass
class ServoTuningParamsetResponse:

    paramset: ServoTuningParamset = next(first for first in ServoTuningParamset)

    @staticmethod
    def zero_values() -> 'ServoTuningParamsetResponse':
        return ServoTuningParamsetResponse(
            paramset=next(first for first in ServoTuningParamset),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ServoTuningParamsetResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ServoTuningParamsetResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'paramset': self.paramset.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ServoTuningParamsetResponse':
        return ServoTuningParamsetResponse(
            paramset=ServoTuningParamset(data.get('paramset')),  # type: ignore
        )
