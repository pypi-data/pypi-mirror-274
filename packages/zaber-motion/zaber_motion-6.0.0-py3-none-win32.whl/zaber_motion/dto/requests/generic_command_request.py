# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class GenericCommandRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    command: str = ""

    check_errors: bool = False

    timeout: int = 0

    @staticmethod
    def zero_values() -> 'GenericCommandRequest':
        return GenericCommandRequest(
            interface_id=0,
            device=0,
            axis=0,
            command="",
            check_errors=False,
            timeout=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GenericCommandRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GenericCommandRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'command': self.command,
            'checkErrors': self.check_errors,
            'timeout': self.timeout,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GenericCommandRequest':
        return GenericCommandRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            command=data.get('command'),  # type: ignore
            check_errors=data.get('checkErrors'),  # type: ignore
            timeout=data.get('timeout'),  # type: ignore
        )
