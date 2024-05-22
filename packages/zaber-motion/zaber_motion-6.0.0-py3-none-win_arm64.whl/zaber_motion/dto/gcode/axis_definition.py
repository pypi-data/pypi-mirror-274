# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class AxisDefinition:
    """
    Defines an axis of the translator.
    """

    peripheral_id: int
    """
    ID of the peripheral.
    """

    microstep_resolution: Optional[int] = None
    """
    Microstep resolution of the axis.
    Can be obtained by reading the resolution setting.
    Leave empty if the axis does not have the setting.
    """

    @staticmethod
    def zero_values() -> 'AxisDefinition':
        return AxisDefinition(
            peripheral_id=0,
            microstep_resolution=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxisDefinition':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxisDefinition.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'peripheralId': self.peripheral_id,
            'microstepResolution': self.microstep_resolution,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxisDefinition':
        return AxisDefinition(
            peripheral_id=data.get('peripheralId'),  # type: ignore
            microstep_resolution=data.get('microstepResolution'),  # type: ignore
        )
