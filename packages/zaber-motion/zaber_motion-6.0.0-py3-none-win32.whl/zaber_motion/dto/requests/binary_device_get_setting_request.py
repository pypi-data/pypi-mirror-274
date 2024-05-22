# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..binary.binary_settings import BinarySettings
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class BinaryDeviceGetSettingRequest:

    interface_id: int = 0

    device: int = 0

    setting: BinarySettings = next(first for first in BinarySettings)

    unit: UnitsAndLiterals = Units.NATIVE

    @staticmethod
    def zero_values() -> 'BinaryDeviceGetSettingRequest':
        return BinaryDeviceGetSettingRequest(
            interface_id=0,
            device=0,
            setting=next(first for first in BinarySettings),
            unit=Units.NATIVE,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'BinaryDeviceGetSettingRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return BinaryDeviceGetSettingRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'setting': self.setting.value,
            'unit': units_from_literals(self.unit).value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BinaryDeviceGetSettingRequest':
        return BinaryDeviceGetSettingRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            setting=BinarySettings(data.get('setting')),  # type: ignore
            unit=Units(data.get('unit')),  # type: ignore
        )
