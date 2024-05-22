# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TestEvent:

    data: str = ""

    @staticmethod
    def zero_values() -> 'TestEvent':
        return TestEvent(
            data="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TestEvent':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TestEvent.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'data': self.data,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TestEvent':
        return TestEvent(
            data=data.get('data'),  # type: ignore
        )
