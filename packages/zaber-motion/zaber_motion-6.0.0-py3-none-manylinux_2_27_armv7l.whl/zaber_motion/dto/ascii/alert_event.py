# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class AlertEvent:
    """
    Alert message received from the device.
    """

    device_address: int
    """
    Number of the device that sent the message.
    """

    axis_number: int
    """
    Number of the axis which the response applies to. Zero denotes device scope.
    """

    status: str
    """
    The device status contains BUSY when the axis is moving and IDLE otherwise.
    """

    warning_flag: str
    """
    The warning flag contains the highest priority warning currently active for the device or axis.
    """

    data: str
    """
    Response data which varies depending on the request.
    """

    @staticmethod
    def zero_values() -> 'AlertEvent':
        return AlertEvent(
            device_address=0,
            axis_number=0,
            status="",
            warning_flag="",
            data="",
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'AlertEvent':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return AlertEvent.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceAddress': self.device_address,
            'axisNumber': self.axis_number,
            'status': self.status,
            'warningFlag': self.warning_flag,
            'data': self.data,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AlertEvent':
        return AlertEvent(
            device_address=data.get('deviceAddress'),  # type: ignore
            axis_number=data.get('axisNumber'),  # type: ignore
            status=data.get('status'),  # type: ignore
            warning_flag=data.get('warningFlag'),  # type: ignore
            data=data.get('data'),  # type: ignore
        )
