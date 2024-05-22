# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class Measurement:
    """
    Represents a numerical value with optional units specified.
    """

    value: float
    """
    Value of the measurement.
    """

    unit: Optional[UnitsAndLiterals] = None
    """
    Optional units of the measurement.
    """

    @staticmethod
    def zero_values() -> 'Measurement':
        return Measurement(
            value=0,
            unit=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'Measurement':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return Measurement.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'value': self.value,
            'unit': units_from_literals(self.unit).value if self.unit is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Measurement':
        return Measurement(
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')) if data.get('unit') is not None else None,  # type: ignore
        )
