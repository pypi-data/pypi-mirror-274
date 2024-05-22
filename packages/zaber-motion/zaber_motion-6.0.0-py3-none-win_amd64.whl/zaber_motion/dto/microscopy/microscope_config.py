# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..axis_address import AxisAddress


@dataclass
class MicroscopeConfig:
    """
    Configuration representing a microscope setup.
    Device address of value 0 means that the part is not present.
    """

    focus_axis: Optional[AxisAddress] = None
    """
    Focus axis of the microscope.
    """

    x_axis: Optional[AxisAddress] = None
    """
    X axis of the microscope.
    """

    y_axis: Optional[AxisAddress] = None
    """
    Y axis of the microscope.
    """

    illuminator: Optional[int] = None
    """
    Illuminator device address.
    """

    filter_changer: Optional[int] = None
    """
    Filter changer device address.
    """

    objective_changer: Optional[int] = None
    """
    Objective changer device address.
    """

    @staticmethod
    def zero_values() -> 'MicroscopeConfig':
        return MicroscopeConfig(
            focus_axis=None,
            x_axis=None,
            y_axis=None,
            illuminator=None,
            filter_changer=None,
            objective_changer=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'MicroscopeConfig':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return MicroscopeConfig.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'focusAxis': self.focus_axis.to_dict() if self.focus_axis is not None else None,
            'xAxis': self.x_axis.to_dict() if self.x_axis is not None else None,
            'yAxis': self.y_axis.to_dict() if self.y_axis is not None else None,
            'illuminator': self.illuminator,
            'filterChanger': self.filter_changer,
            'objectiveChanger': self.objective_changer,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MicroscopeConfig':
        return MicroscopeConfig(
            focus_axis=AxisAddress.from_dict(data.get('focusAxis')) if data.get('focusAxis') is not None else None,  # type: ignore
            x_axis=AxisAddress.from_dict(data.get('xAxis')) if data.get('xAxis') is not None else None,  # type: ignore
            y_axis=AxisAddress.from_dict(data.get('yAxis')) if data.get('yAxis') is not None else None,  # type: ignore
            illuminator=data.get('illuminator'),  # type: ignore
            filter_changer=data.get('filterChanger'),  # type: ignore
            objective_changer=data.get('objectiveChanger'),  # type: ignore
        )
