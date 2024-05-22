# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TestResponseLong:

    data_pong: List[str] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'TestResponseLong':
        return TestResponseLong(
            data_pong=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TestResponseLong':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TestResponseLong.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'dataPong': self.data_pong,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TestResponseLong':
        return TestResponseLong(
            data_pong=data.get('dataPong'),  # type: ignore
        )
