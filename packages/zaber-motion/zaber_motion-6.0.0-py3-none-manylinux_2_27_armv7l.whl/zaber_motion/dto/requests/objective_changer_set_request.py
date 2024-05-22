# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class ObjectiveChangerSetRequest:

    interface_id: int = 0

    turret_address: int = 0

    focus_address: int = 0

    focus_axis: int = 0

    value: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'ObjectiveChangerSetRequest':
        return ObjectiveChangerSetRequest(
            interface_id=0,
            turret_address=0,
            focus_address=0,
            focus_axis=0,
            value=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ObjectiveChangerSetRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ObjectiveChangerSetRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'turretAddress': self.turret_address,
            'focusAddress': self.focus_address,
            'focusAxis': self.focus_axis,
            'value': self.value,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ObjectiveChangerSetRequest':
        return ObjectiveChangerSetRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            turret_address=data.get('turretAddress'),  # type: ignore
            focus_address=data.get('focusAddress'),  # type: ignore
            focus_axis=data.get('focusAxis'),  # type: ignore
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
