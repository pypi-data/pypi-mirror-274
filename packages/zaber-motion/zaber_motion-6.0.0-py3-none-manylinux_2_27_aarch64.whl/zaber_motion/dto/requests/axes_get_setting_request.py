# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ...units import Units, UnitsAndLiterals, units_from_literals


@dataclass
class AxesGetSettingRequest:

    interfaces: List[int] = field(default_factory=list)

    devices: List[int] = field(default_factory=list)

    axes: List[int] = field(default_factory=list)

    unit: List[UnitsAndLiterals] = field(default_factory=list)

    setting: str = ""

    @staticmethod
    def zero_values() -> 'AxesGetSettingRequest':
        return AxesGetSettingRequest(
            interfaces=[],
            devices=[],
            axes=[],
            unit=[],
            setting="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AxesGetSettingRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AxesGetSettingRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaces': self.interfaces,
            'devices': self.devices,
            'axes': self.axes,
            'unit': [units_from_literals(item).value for item in self.unit],
            'setting': self.setting,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AxesGetSettingRequest':
        return AxesGetSettingRequest(
            interfaces=data.get('interfaces'),  # type: ignore
            devices=data.get('devices'),  # type: ignore
            axes=data.get('axes'),  # type: ignore
            unit=[Units(item) for item in data.get('unit')],  # type: ignore
            setting=data.get('setting'),  # type: ignore
        )
