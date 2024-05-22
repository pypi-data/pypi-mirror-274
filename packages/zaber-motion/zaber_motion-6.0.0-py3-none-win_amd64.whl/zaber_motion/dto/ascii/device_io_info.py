# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class DeviceIOInfo:
    """
    Class representing information on the I/O channels of the device.
    """

    number_analog_outputs: int
    """
    Number of analog output channels.
    """

    number_analog_inputs: int
    """
    Number of analog input channels.
    """

    number_digital_outputs: int
    """
    Number of digital output channels.
    """

    number_digital_inputs: int
    """
    Number of digital input channels.
    """

    @staticmethod
    def zero_values() -> 'DeviceIOInfo':
        return DeviceIOInfo(
            number_analog_outputs=0,
            number_analog_inputs=0,
            number_digital_outputs=0,
            number_digital_inputs=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'DeviceIOInfo':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return DeviceIOInfo.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'numberAnalogOutputs': self.number_analog_outputs,
            'numberAnalogInputs': self.number_analog_inputs,
            'numberDigitalOutputs': self.number_digital_outputs,
            'numberDigitalInputs': self.number_digital_inputs,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DeviceIOInfo':
        return DeviceIOInfo(
            number_analog_outputs=data.get('numberAnalogOutputs'),  # type: ignore
            number_analog_inputs=data.get('numberAnalogInputs'),  # type: ignore
            number_digital_outputs=data.get('numberDigitalOutputs'),  # type: ignore
            number_digital_inputs=data.get('numberDigitalInputs'),  # type: ignore
        )
