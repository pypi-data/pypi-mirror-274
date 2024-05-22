# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class GetSetting:
    """
    Specifies a setting to get with one of the multi-get commands.
    """

    setting: str
    """
    The setting to read.
    """

    axes: Optional[List[int]] = None
    """
    The list of axes to read.
    """

    unit: Optional[UnitsAndLiterals] = None
    """
    The unit to convert the read settings to.
    """

    @staticmethod
    def zero_values() -> 'GetSetting':
        return GetSetting(
            setting="",
            axes=None,
            unit=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetSetting':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetSetting.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'setting': self.setting,
            'axes': self.axes,
            'unit': units_from_literals(self.unit).value if self.unit is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetSetting':
        return GetSetting(
            setting=data.get('setting'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
            unit=Units(data.get('unit')) if data.get('unit') is not None else None,  # type: ignore
        )
