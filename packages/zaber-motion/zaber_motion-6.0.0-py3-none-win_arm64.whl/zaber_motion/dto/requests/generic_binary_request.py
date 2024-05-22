# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..binary.command_code import CommandCode


@dataclass
class GenericBinaryRequest:

    interface_id: int = 0

    device: int = 0

    command: CommandCode = next(first for first in CommandCode)

    data: int = 0

    check_errors: bool = False

    timeout: float = 0

    @staticmethod
    def zero_values() -> 'GenericBinaryRequest':
        return GenericBinaryRequest(
            interface_id=0,
            device=0,
            command=next(first for first in CommandCode),
            data=0,
            check_errors=False,
            timeout=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GenericBinaryRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GenericBinaryRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'command': self.command.value,
            'data': self.data,
            'checkErrors': self.check_errors,
            'timeout': self.timeout,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GenericBinaryRequest':
        return GenericBinaryRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            command=CommandCode(data.get('command')),  # type: ignore
            data=data.get('data'),  # type: ignore
            check_errors=data.get('checkErrors'),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
        )
