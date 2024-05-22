# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .axis_move_type import AxisMoveType
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class LockstepMoveRequest:

    interface_id: int = 0

    device: int = 0

    lockstep_group_id: int = 0

    wait_until_idle: bool = False

    type: AxisMoveType = next(first for first in AxisMoveType)

    arg: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    velocity: float = 0

    velocity_unit: UnitsAndLiterals = Units.NATIVE

    acceleration: float = 0

    acceleration_unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'LockstepMoveRequest':
        return LockstepMoveRequest(
            interface_id=0,
            device=0,
            lockstep_group_id=0,
            wait_until_idle=False,
            type=next(first for first in AxisMoveType),
            arg=0,
            unit=Units.NATIVE,
            velocity=0,
            velocity_unit=Units.NATIVE,
            acceleration=0,
            acceleration_unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepMoveRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepMoveRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'lockstepGroupId': self.lockstep_group_id,
            'waitUntilIdle': self.wait_until_idle,
            'type': self.type.value,
            'arg': self.arg,
            'unit': units_from_literals(self.unit).value,
            'velocity': self.velocity,
            'velocityUnit': units_from_literals(self.velocity_unit).value,
            'acceleration': self.acceleration,
            'accelerationUnit': units_from_literals(self.acceleration_unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepMoveRequest':
        return LockstepMoveRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            lockstep_group_id=data.get('lockstepGroupId'),  # type: ignore
            wait_until_idle=data.get('waitUntilIdle'),  # type: ignore
            type=AxisMoveType(data.get('type')),  # type: ignore
            arg=data.get('arg'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
            velocity=data.get('velocity'),  # type: ignore
            velocity_unit=Units(data.get('velocityUnit')),  # type: ignore
            acceleration=data.get('acceleration'),  # type: ignore
            acceleration_unit=Units(data.get('accelerationUnit')),  # type: ignore
        )
