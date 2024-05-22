# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class LockstepAxes:
    """
    The axis numbers of a lockstep group.
    """

    axis_1: int
    """
    The axis number used to set the first axis.
    """

    axis_2: int
    """
    The axis number used to set the second axis.
    """

    axis_3: int
    """
    The axis number used to set the third axis.
    """

    axis_4: int
    """
    The axis number used to set the fourth axis.
    """

    @staticmethod
    def zero_values() -> 'LockstepAxes':
        return LockstepAxes(
            axis_1=0,
            axis_2=0,
            axis_3=0,
            axis_4=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepAxes':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepAxes.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axis1': self.axis_1,
            'axis2': self.axis_2,
            'axis3': self.axis_3,
            'axis4': self.axis_4,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepAxes':
        return LockstepAxes(
            axis_1=data.get('axis1'),  # type: ignore
            axis_2=data.get('axis2'),  # type: ignore
            axis_3=data.get('axis3'),  # type: ignore
            axis_4=data.get('axis4'),  # type: ignore
        )
