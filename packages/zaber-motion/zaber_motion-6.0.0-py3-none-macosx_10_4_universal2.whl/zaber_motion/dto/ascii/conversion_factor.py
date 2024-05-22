# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class ConversionFactor:
    """
    Represents unit conversion factor for a single dimension.
    """

    setting: str
    """
    Setting representing the dimension.
    """

    value: float
    """
    Value representing 1 native device unit in specified real-word units.
    """

    unit: UnitsAndLiterals
    """
    Units of the value.
    """

    @staticmethod
    def zero_values() -> 'ConversionFactor':
        return ConversionFactor(
            setting="",
            value=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ConversionFactor':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ConversionFactor.from_dict(data)

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
    def from_dict(data: Dict[str, Any]) -> 'ConversionFactor':
        return ConversionFactor(
            setting=data.get('setting'),  # type: ignore
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
