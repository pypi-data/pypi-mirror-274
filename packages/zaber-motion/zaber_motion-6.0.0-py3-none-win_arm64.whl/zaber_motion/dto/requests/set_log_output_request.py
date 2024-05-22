# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..log_output_mode import LogOutputMode


@dataclass
class SetLogOutputRequest:

    mode: LogOutputMode = next(first for first in LogOutputMode)

    file_path: str = ""

    @staticmethod
    def zero_values() -> 'SetLogOutputRequest':
        return SetLogOutputRequest(
            mode=next(first for first in LogOutputMode),
            file_path="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetLogOutputRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetLogOutputRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'mode': self.mode.value,
            'filePath': self.file_path,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetLogOutputRequest':
        return SetLogOutputRequest(
            mode=LogOutputMode(data.get('mode')),  # type: ignore
            file_path=data.get('filePath'),  # type: ignore
        )
