# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .translate_message import TranslateMessage


@dataclass
class TranslateResult:
    """
    Represents a result of a G-code block translation.
    """

    commands: List[str]
    """
    Stream commands resulting from the block.
    """

    warnings: List[TranslateMessage]
    """
    Messages informing about unsupported codes and features.
    """

    @staticmethod
    def zero_values() -> 'TranslateResult':
        return TranslateResult(
            commands=[],
            warnings=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslateResult':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslateResult.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'commands': self.commands,
            'warnings': [item.to_dict() for item in self.warnings],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslateResult':
        return TranslateResult(
            commands=data.get('commands'),  # type: ignore
            warnings=[TranslateMessage.from_dict(item) for item in data.get('warnings')],  # type: ignore
        )
