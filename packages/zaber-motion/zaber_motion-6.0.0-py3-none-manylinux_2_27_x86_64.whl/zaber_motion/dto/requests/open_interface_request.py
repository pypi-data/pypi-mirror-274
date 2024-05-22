# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .interface_type import InterfaceType


@dataclass
class OpenInterfaceRequest:

    interface_type: InterfaceType = next(first for first in InterfaceType)

    port_name: str = ""

    baud_rate: int = 0

    host_name: str = ""

    port: int = 0

    transport: int = 0

    reject_routed_connection: bool = False

    cloud_id: str = ""

    connection_name: str = ""

    realm: str = ""

    token: str = ""

    api: str = ""

    @staticmethod
    def zero_values() -> 'OpenInterfaceRequest':
        return OpenInterfaceRequest(
            interface_type=next(first for first in InterfaceType),
            port_name="",
            baud_rate=0,
            host_name="",
            port=0,
            transport=0,
            reject_routed_connection=False,
            cloud_id="",
            connection_name="",
            realm="",
            token="",
            api="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OpenInterfaceRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OpenInterfaceRequest.from_dict(data)

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
            'transport': self.transport,
            'rejectRoutedConnection': self.reject_routed_connection,
            'cloudId': self.cloud_id,
            'connectionName': self.connection_name,
            'realm': self.realm,
            'token': self.token,
            'api': self.api,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OpenInterfaceRequest':
        return OpenInterfaceRequest(
            interface_type=InterfaceType(data.get('interfaceType')),  # type: ignore
            port_name=data.get('portName'),  # type: ignore
            baud_rate=data.get('baudRate'),  # type: ignore
            host_name=data.get('hostName'),  # type: ignore
            port=data.get('port'),  # type: ignore
            transport=data.get('transport'),  # type: ignore
            reject_routed_connection=data.get('rejectRoutedConnection'),  # type: ignore
            cloud_id=data.get('cloudId'),  # type: ignore
            connection_name=data.get('connectionName'),  # type: ignore
            realm=data.get('realm'),  # type: ignore
            token=data.get('token'),  # type: ignore
            api=data.get('api'),  # type: ignore
        )
