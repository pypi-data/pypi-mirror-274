# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class SetPeripheralStateExceptionData:
    """
    Contains additional data for a SetPeripheralStateFailedException.
    """

    axis_number: int
    """
    The number of axis where the exception originated.
    """

    settings: List[str]
    """
    A list of settings which could not be set.
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

    @staticmethod
    def zero_values() -> 'SetPeripheralStateExceptionData':
        return SetPeripheralStateExceptionData(
            axis_number=0,
            settings=[],
            servo_tuning="",
            stored_positions=[],
            storage=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SetPeripheralStateExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SetPeripheralStateExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axisNumber': self.axis_number,
            'settings': self.settings,
            'servoTuning': self.servo_tuning,
            'storedPositions': self.stored_positions,
            'storage': self.storage,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SetPeripheralStateExceptionData':
        return SetPeripheralStateExceptionData(
            axis_number=data.get('axisNumber'),  # type: ignore
            settings=data.get('settings'),  # type: ignore
            servo_tuning=data.get('servoTuning'),  # type: ignore
            stored_positions=data.get('storedPositions'),  # type: ignore
            storage=data.get('storage'),  # type: ignore
        )
