# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class LockstepSetRequest:

    interface_id: int = 0

    device: int = 0

    lockstep_group_id: int = 0

    value: float = 0

    unit: UnitsAndLiterals = Units.NATIVE

    axis_index: int = 0

    @staticmethod
    def zero_values() -> 'LockstepSetRequest':
        return LockstepSetRequest(
            interface_id=0,
            device=0,
            lockstep_group_id=0,
            value=0,
            unit=Units.NATIVE,
            axis_index=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'LockstepSetRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return LockstepSetRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'lockstepGroupId': self.lockstep_group_id,
            'value': self.value,
            'unit': units_from_literals(self.unit).value,
            'axisIndex': self.axis_index,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LockstepSetRequest':
        return LockstepSetRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            lockstep_group_id=data.get('lockstepGroupId'),  # type: ignore
            value=data.get('value'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
            axis_index=data.get('axisIndex'),  # type: ignore
        )
