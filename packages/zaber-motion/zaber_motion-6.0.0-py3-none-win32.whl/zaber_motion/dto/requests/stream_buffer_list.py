# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class StreamBufferList:

    interface_id: int = 0

    device: int = 0

    pvt: bool = False

    @staticmethod
    def zero_values() -> 'StreamBufferList':
        return StreamBufferList(
            interface_id=0,
            device=0,
            pvt=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamBufferList':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamBufferList.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'pvt': self.pvt,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamBufferList':
        return StreamBufferList(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            pvt=data.get('pvt'),  # type: ignore
        )
