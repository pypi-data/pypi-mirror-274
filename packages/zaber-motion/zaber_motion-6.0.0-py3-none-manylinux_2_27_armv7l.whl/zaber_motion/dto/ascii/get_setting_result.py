# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class GetSettingResult:
    """
    The response from a multi-get command.
    """

    setting: str
    """
    The setting read.
    """

    values: List[float]
    """
    The list of values returned.
    """

    unit: UnitsAndLiterals
    """
    The unit of the values.
    """

    @staticmethod
    def zero_values() -> 'GetSettingResult':
        return GetSettingResult(
            setting="",
            values=[],
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetSettingResult':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetSettingResult.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'setting': self.setting,
            'values': self.values,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetSettingResult':
        return GetSettingResult(
            setting=data.get('setting'),  # type: ignore
            values=data.get('values'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
