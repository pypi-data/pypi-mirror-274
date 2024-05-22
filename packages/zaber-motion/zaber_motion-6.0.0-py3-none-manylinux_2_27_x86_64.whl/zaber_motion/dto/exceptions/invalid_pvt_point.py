# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class InvalidPvtPoint:
    """
    Contains invalid PVT points for PvtExecutionException.
    """

    index: int
    """
    Index of the point numbered from the last submitted point.
    """

    point: str
    """
    The textual representation of the point.
    """

    @staticmethod
    def zero_values() -> 'InvalidPvtPoint':
        return InvalidPvtPoint(
            index=0,
            point="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'InvalidPvtPoint':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return InvalidPvtPoint.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'point': self.point,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'InvalidPvtPoint':
        return InvalidPvtPoint(
            index=data.get('index'),  # type: ignore
            point=data.get('point'),  # type: ignore
        )
