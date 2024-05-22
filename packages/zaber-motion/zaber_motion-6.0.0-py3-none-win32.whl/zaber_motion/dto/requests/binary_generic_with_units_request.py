# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..binary.command_code import CommandCode
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class BinaryGenericWithUnitsRequest:

    interface_id: int = 0

    device: int = 0

    command: CommandCode = next(first for first in CommandCode)

    data: float = 0

    from_unit: UnitsAndLiterals = Units.NATIVE

    to_unit: UnitsAndLiterals = Units.NATIVE

    timeout: float = 0

    @staticmethod
    def zero_values() -> 'BinaryGenericWithUnitsRequest':
        return BinaryGenericWithUnitsRequest(
            interface_id=0,
            device=0,
            command=next(first for first in CommandCode),
            data=0,
            from_unit=Units.NATIVE,
            to_unit=Units.NATIVE,
            timeout=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryGenericWithUnitsRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryGenericWithUnitsRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'command': self.command.value,
            'data': self.data,
            'fromUnit': units_from_literals(self.from_unit).value,
            'toUnit': units_from_literals(self.to_unit).value,
            'timeout': self.timeout,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryGenericWithUnitsRequest':
        return BinaryGenericWithUnitsRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            command=CommandCode(data.get('command')),  # type: ignore
            data=data.get('data'),  # type: ignore
            from_unit=Units(data.get('fromUnit')),  # type: ignore
            to_unit=Units(data.get('toUnit')),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
        )
