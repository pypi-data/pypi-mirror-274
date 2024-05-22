# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .servo_tuning_param import ServoTuningParam


@dataclass
class ParamsetInfo:
    """
    The raw parameters currently saved to a given paramset.
    """

    type: str
    """
    The tuning algorithm used for this axis.
    """

    version: int
    """
    The version of the tuning algorithm used for this axis.
    """

    params: List[ServoTuningParam]
    """
    The raw tuning parameters of this device.
    """

    @staticmethod
    def zero_values() -> 'ParamsetInfo':
        return ParamsetInfo(
            type="",
            version=0,
            params=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ParamsetInfo':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ParamsetInfo.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'version': self.version,
            'params': [item.to_dict() for item in self.params],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ParamsetInfo':
        return ParamsetInfo(
            type=data.get('type'),  # type: ignore
            version=data.get('version'),  # type: ignore
            params=[ServoTuningParam.from_dict(item) for item in data.get('params')],  # type: ignore
        )
