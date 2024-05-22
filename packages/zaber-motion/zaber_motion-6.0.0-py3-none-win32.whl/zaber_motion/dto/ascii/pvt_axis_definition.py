# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .pvt_axis_type import PvtAxisType


@dataclass
class PvtAxisDefinition:
    """
    Defines an axis of the PVT sequence.
    """

    axis_number: int
    """
    Number of a physical axis or a lockstep group.
    """

    axis_type: Optional[PvtAxisType] = None
    """
    Defines the type of the axis.
    """

    @staticmethod
    def zero_values() -> 'PvtAxisDefinition':
        return PvtAxisDefinition(
            axis_number=0,
            axis_type=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PvtAxisDefinition':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PvtAxisDefinition.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axisNumber': self.axis_number,
            'axisType': self.axis_type.value if self.axis_type is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PvtAxisDefinition':
        return PvtAxisDefinition(
            axis_number=data.get('axisNumber'),  # type: ignore
            axis_type=PvtAxisType(data.get('axisType')) if data.get('axisType') is not None else None,  # type: ignore
        )
