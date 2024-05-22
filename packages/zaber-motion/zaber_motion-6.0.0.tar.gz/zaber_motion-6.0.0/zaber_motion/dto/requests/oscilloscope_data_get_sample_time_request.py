# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class OscilloscopeDataGetSampleTimeRequest:

    data_id: int = 0

    unit: UnitsAndLiterals = Units.NATIVE

    index: int = 0

    @staticmethod
    def zero_values() -> 'OscilloscopeDataGetSampleTimeRequest':
        return OscilloscopeDataGetSampleTimeRequest(
            data_id=0,
            unit=Units.NATIVE,
            index=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OscilloscopeDataGetSampleTimeRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OscilloscopeDataGetSampleTimeRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'dataId': self.data_id,
            'unit': units_from_literals(self.unit).value,
            'index': self.index,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OscilloscopeDataGetSampleTimeRequest':
        return OscilloscopeDataGetSampleTimeRequest(
            data_id=data.get('dataId'),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
            index=data.get('index'),  # type: ignore
        )
