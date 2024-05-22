# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .axis_move_type import AxisMoveType
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class BinaryDeviceMoveRequest:

    interface_id: int = 0

    device: int = 0

    timeout: float = 0

    type: AxisMoveType = next(first for first in AxisMoveType)

    arg: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'BinaryDeviceMoveRequest':
        return BinaryDeviceMoveRequest(
            interface_id=0,
            device=0,
            timeout=0,
            type=next(first for first in AxisMoveType),
            arg=0,
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryDeviceMoveRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryDeviceMoveRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'timeout': self.timeout,
            'type': self.type.value,
            'arg': self.arg,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryDeviceMoveRequest':
        return BinaryDeviceMoveRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
            type=AxisMoveType(data.get('type')),  # type: ignore
            arg=data.get('arg'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
