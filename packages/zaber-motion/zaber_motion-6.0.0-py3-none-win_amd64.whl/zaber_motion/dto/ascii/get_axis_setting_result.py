# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class GetAxisSettingResult:
    """
    The response from a multi-get axis command.
    """

    setting: str
    """
    The setting read.
    """

    value: float
    """
    The value read.
    """

    unit: UnitsAndLiterals
    """
    The unit of the values.
    """

    @staticmethod
    def zero_values() -> 'GetAxisSettingResult':
        return GetAxisSettingResult(
            setting="",
            value=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetAxisSettingResult':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetAxisSettingResult.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'setting': self.setting,
            'value': self.value,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetAxisSettingResult':
        return GetAxisSettingResult(
            setting=data.get('setting'),  # type: ignore
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
