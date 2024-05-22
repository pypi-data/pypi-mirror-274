# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.get_setting_result import GetSettingResult


@dataclass
class GetSettingResults:

    results: List[GetSettingResult] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'GetSettingResults':
        return GetSettingResults(
            results=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetSettingResults':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetSettingResults.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'results': [item.to_dict() for item in self.results],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetSettingResults':
        return GetSettingResults(
            results=[GetSettingResult.from_dict(item) for item in data.get('results')],  # type: ignore
        )
