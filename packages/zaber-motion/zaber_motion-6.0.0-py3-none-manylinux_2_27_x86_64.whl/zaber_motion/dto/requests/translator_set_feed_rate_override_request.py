# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TranslatorSetFeedRateOverrideRequest:

    translator_id: int = 0

    coefficient: float = 0

    @staticmethod
    def zero_values() -> 'TranslatorSetFeedRateOverrideRequest':
        return TranslatorSetFeedRateOverrideRequest(
            translator_id=0,
            coefficient=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorSetFeedRateOverrideRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorSetFeedRateOverrideRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'translatorId': self.translator_id,
            'coefficient': self.coefficient,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorSetFeedRateOverrideRequest':
        return TranslatorSetFeedRateOverrideRequest(
            translator_id=data.get('translatorId'),  # type: ignore
            coefficient=data.get('coefficient'),  # type: ignore
        )
