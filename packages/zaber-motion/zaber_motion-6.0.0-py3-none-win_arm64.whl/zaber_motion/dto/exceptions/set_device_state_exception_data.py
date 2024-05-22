# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .set_peripheral_state_exception_data import SetPeripheralStateExceptionData


@dataclass
class SetDeviceStateExceptionData:
    """
    Contains additional data for a SetDeviceStateFailedException.
    """

    settings: List[str]
    """
    A list of settings which could not be set.
    """

    stream_buffers: List[str]
    """
    The reason the stream buffers could not be set.
    """

    pvt_buffers: List[str]
    """
    The reason the pvt buffers could not be set.
    """

    triggers: List[str]
    """
    The reason the triggers could not be set.
    """

    servo_tuning: str
    """
    The reason servo tuning could not be set.
    """

    stored_positions: List[str]
    """
    The reasons stored positions could not be set.
    """

    storage: List[str]
    """
    The reasons storage could not be set.
    """

    peripherals: List[SetPeripheralStateExceptionData]
    """
    Errors for any peripherals that could not be set.
    """

    @staticmethod
    def zero_values() -> 'SetDeviceStateExceptionData':
        return SetDeviceStateExceptionData(
            settings=[],
            stream_buffers=[],
            pvt_buffers=[],
            triggers=[],
            servo_tuning="",
            stored_positions=[],
            storage=[],
            peripherals=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetDeviceStateExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetDeviceStateExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'settings': self.settings,
            'streamBuffers': self.stream_buffers,
            'pvtBuffers': self.pvt_buffers,
            'triggers': self.triggers,
            'servoTuning': self.servo_tuning,
            'storedPositions': self.stored_positions,
            'storage': self.storage,
            'peripherals': [item.to_dict() for item in self.peripherals],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetDeviceStateExceptionData':
        return SetDeviceStateExceptionData(
            settings=data.get('settings'),  # type: ignore
            stream_buffers=data.get('streamBuffers'),  # type: ignore
            pvt_buffers=data.get('pvtBuffers'),  # type: ignore
            triggers=data.get('triggers'),  # type: ignore
            servo_tuning=data.get('servoTuning'),  # type: ignore
            stored_positions=data.get('storedPositions'),  # type: ignore
            storage=data.get('storage'),  # type: ignore
            peripherals=[SetPeripheralStateExceptionData.from_dict(item) for item in data.get('peripherals')],  # type: ignore
        )
