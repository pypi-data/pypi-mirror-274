# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .interface_type import InterfaceType


@dataclass
class OpenBinaryInterfaceRequest:

    interface_type: InterfaceType = next(first for first in InterfaceType)

    port_name: str = ""

    baud_rate: int = 0

    host_name: str = ""

    port: int = 0

    use_message_ids: bool = False

    @staticmethod
    def zero_values() -> 'OpenBinaryInterfaceRequest':
        return OpenBinaryInterfaceRequest(
            interface_type=next(first for first in InterfaceType),
            port_name="",
            baud_rate=0,
            host_name="",
            port=0,
            use_message_ids=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OpenBinaryInterfaceRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OpenBinaryInterfaceRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceType': self.interface_type.value,
            'portName': self.port_name,
            'baudRate': self.baud_rate,
            'hostName': self.host_name,
            'port': self.port,
            'useMessageIds': self.use_message_ids,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OpenBinaryInterfaceRequest':
        return OpenBinaryInterfaceRequest(
            interface_type=InterfaceType(data.get('interfaceType')),  # type: ignore
            port_name=data.get('portName'),  # type: ignore
            baud_rate=data.get('baudRate'),  # type: ignore
            host_name=data.get('hostName'),  # type: ignore
            port=data.get('port'),  # type: ignore
            use_message_ids=data.get('useMessageIds'),  # type: ignore
        )
