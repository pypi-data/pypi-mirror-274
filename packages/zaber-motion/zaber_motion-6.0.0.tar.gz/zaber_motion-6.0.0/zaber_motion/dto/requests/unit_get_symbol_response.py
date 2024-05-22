# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class UnitGetSymbolResponse:

    symbol: str = ""

    @staticmethod
    def zero_values() -> 'UnitGetSymbolResponse':
        return UnitGetSymbolResponse(
            symbol="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnitGetSymbolResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnitGetSymbolResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnitGetSymbolResponse':
        return UnitGetSymbolResponse(
            symbol=data.get('symbol'),  # type: ignore
        )
