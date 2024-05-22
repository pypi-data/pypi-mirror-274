# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.get_setting import GetSetting
from ..ascii.get_axis_setting import GetAxisSetting


@dataclass
class DeviceMultiGetSettingRequest:

    interface_id: int = 0

    device: int = 0

    axis: int = 0

    settings: List[GetSetting] = field(default_factory=list)

    axis_settings: List[GetAxisSetting] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'DeviceMultiGetSettingRequest':
        return DeviceMultiGetSettingRequest(
            interface_id=0,
            device=0,
            axis=0,
            settings=[],
            axis_settings=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceMultiGetSettingRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceMultiGetSettingRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'axis': self.axis,
            'settings': [item.to_dict() for item in self.settings],
            'axisSettings': [item.to_dict() for item in self.axis_settings],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceMultiGetSettingRequest':
        return DeviceMultiGetSettingRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            axis=data.get('axis'),  # type: ignore
            settings=[GetSetting.from_dict(item) for item in data.get('settings')],  # type: ignore
            axis_settings=[GetAxisSetting.from_dict(item) for item in data.get('axisSettings')],  # type: ignore
        )
