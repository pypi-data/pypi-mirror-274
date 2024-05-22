# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .oscilloscope_data_source import OscilloscopeDataSource
from .io_port_type import IoPortType


@dataclass
class OscilloscopeCaptureProperties:
    """
    The public properties of one channel of recorded oscilloscope data.
    """

    data_source: OscilloscopeDataSource
    """
    Indicates whether the data came from a setting or an I/O pin.
    """

    setting: str
    """
    The name of the recorded setting.
    """

    axis_number: int
    """
    The number of the axis the data was recorded from, or 0 for the controller.
    """

    io_type: IoPortType
    """
    Which kind of I/O port data was recorded from.
    """

    io_channel: int
    """
    Which I/O pin within the port was recorded.
    """

    @staticmethod
    def zero_values() -> 'OscilloscopeCaptureProperties':
        return OscilloscopeCaptureProperties(
            data_source=next(first for first in OscilloscopeDataSource),
            setting="",
            axis_number=0,
            io_type=next(first for first in IoPortType),
            io_channel=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'OscilloscopeCaptureProperties':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return OscilloscopeCaptureProperties.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'dataSource': self.data_source.value,
            'setting': self.setting,
            'axisNumber': self.axis_number,
            'ioType': self.io_type.value,
            'ioChannel': self.io_channel,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'OscilloscopeCaptureProperties':
        return OscilloscopeCaptureProperties(
            data_source=OscilloscopeDataSource(data.get('dataSource')),  # type: ignore
            setting=data.get('setting'),  # type: ignore
            axis_number=data.get('axisNumber'),  # type: ignore
            io_type=IoPortType(data.get('ioType')),  # type: ignore
            io_channel=data.get('ioChannel'),  # type: ignore
        )
