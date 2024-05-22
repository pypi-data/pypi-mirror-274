# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class TranslatorTranslateRequest:

    translator_id: int = 0

    block: str = ""

    @staticmethod
    def zero_values() -> 'TranslatorTranslateRequest':
        return TranslatorTranslateRequest(
            translator_id=0,
            block="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorTranslateRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorTranslateRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'translatorId': self.translator_id,
            'block': self.block,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorTranslateRequest':
        return TranslatorTranslateRequest(
            translator_id=data.get('translatorId'),  # type: ignore
            block=data.get('block'),  # type: ignore
        )
