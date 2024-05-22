# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class PidTuning:
    """
    The tuning of this axis represented by PID parameters.
    """

    type: str
    """
    The tuning algorithm used to tune this axis.
    """

    version: int
    """
    The version of the tuning algorithm used to tune this axis.
    """

    p: float
    """
    The positional tuning argument.
    """

    i: float
    """
    The integral tuning argument.
    """

    d: float
    """
    The derivative tuning argument.
    """

    fc: float
    """
    The frequency cutoff for the tuning.
    """

    @staticmethod
    def zero_values() -> 'PidTuning':
        return PidTuning(
            type="",
            version=0,
            p=0,
            i=0,
            d=0,
            fc=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'PidTuning':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return PidTuning.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'version': self.version,
            'p': self.p,
            'i': self.i,
            'd': self.d,
            'fc': self.fc,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PidTuning':
        return PidTuning(
            type=data.get('type'),  # type: ignore
            version=data.get('version'),  # type: ignore
            p=data.get('p'),  # type: ignore
            i=data.get('i'),  # type: ignore
            d=data.get('d'),  # type: ignore
            fc=data.get('fc'),  # type: ignore
        )
