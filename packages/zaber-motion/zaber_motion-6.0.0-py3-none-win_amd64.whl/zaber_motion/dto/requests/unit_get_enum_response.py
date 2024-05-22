# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class UnitGetEnumResponse:

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'UnitGetEnumResponse':
        return UnitGetEnumResponse(
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnitGetEnumResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnitGetEnumResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnitGetEnumResponse':
        return UnitGetEnumResponse(
            unit=Units(data.get('unit')),  # type: ignore
        )
