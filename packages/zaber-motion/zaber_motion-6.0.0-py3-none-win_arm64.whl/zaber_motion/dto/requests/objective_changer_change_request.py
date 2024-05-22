# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..measurement import Measurement


@dataclass
class ObjectiveChangerChangeRequest:

    interface_id: int = 0

    turret_address: int = 0

    focus_address: int = 0

    focus_axis: int = 0

    objective: int = 0

    focus_offset: Optional[Measurement] = None

    @staticmethod
    def zero_values() -> 'ObjectiveChangerChangeRequest':
        return ObjectiveChangerChangeRequest(
            interface_id=0,
            turret_address=0,
            focus_address=0,
            focus_axis=0,
            objective=0,
            focus_offset=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'ObjectiveChangerChangeRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return ObjectiveChangerChangeRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'turretAddress': self.turret_address,
            'focusAddress': self.focus_address,
            'focusAxis': self.focus_axis,
            'objective': self.objective,
            'focusOffset': self.focus_offset.to_dict() if self.focus_offset is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ObjectiveChangerChangeRequest':
        return ObjectiveChangerChangeRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            turret_address=data.get('turretAddress'),  # type: ignore
            focus_address=data.get('focusAddress'),  # type: ignore
            focus_axis=data.get('focusAxis'),  # type: ignore
            objective=data.get('objective'),  # type: ignore
            focus_offset=Measurement.from_dict(data.get('focusOffset')) if data.get('focusOffset') is not None else None,  # type: ignore
        )
