# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TranslatorFlushLiveRequest:

    translator_id: int = 0

    wait_until_idle: bool = False

    @staticmethod
    def zero_values() -> 'TranslatorFlushLiveRequest':
        return TranslatorFlushLiveRequest(
            translator_id=0,
            wait_until_idle=False,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorFlushLiveRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorFlushLiveRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'translatorId': self.translator_id,
            'waitUntilIdle': self.wait_until_idle,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorFlushLiveRequest':
        return TranslatorFlushLiveRequest(
            translator_id=data.get('translatorId'),  # type: ignore
            wait_until_idle=data.get('waitUntilIdle'),  # type: ignore
        )
