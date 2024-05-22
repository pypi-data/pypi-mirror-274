# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .stream_axis_type import StreamAxisType


@dataclass
class StreamAxisDefinition:
    """
    Defines an axis of the stream.
    """

    axis_number: int
    """
    Number of a physical axis or a lockstep group.
    """

    axis_type: Optional[StreamAxisType] = None
    """
    Defines the type of the axis.
    """

    @staticmethod
    def zero_values() -> 'StreamAxisDefinition':
        return StreamAxisDefinition(
            axis_number=0,
            axis_type=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamAxisDefinition':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamAxisDefinition.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axisNumber': self.axis_number,
            'axisType': self.axis_type.value if self.axis_type is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamAxisDefinition':
        return StreamAxisDefinition(
            axis_number=data.get('axisNumber'),  # type: ignore
            axis_type=StreamAxisType(data.get('axisType')) if data.get('axisType') is not None else None,  # type: ignore
        )
