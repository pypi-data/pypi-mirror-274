# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.stream_mode import StreamMode
from ..ascii.pvt_mode import PvtMode


@dataclass
class StreamModeResponse:

    stream_mode: StreamMode = next(first for first in StreamMode)

    pvt_mode: PvtMode = next(first for first in PvtMode)

    @staticmethod
    def zero_values() -> 'StreamModeResponse':
        return StreamModeResponse(
            stream_mode=next(first for first in StreamMode),
            pvt_mode=next(first for first in PvtMode),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'StreamModeResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return StreamModeResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'streamMode': self.stream_mode.value,
            'pvtMode': self.pvt_mode.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StreamModeResponse':
        return StreamModeResponse(
            stream_mode=StreamMode(data.get('streamMode')),  # type: ignore
            pvt_mode=PvtMode(data.get('pvtMode')),  # type: ignore
        )
