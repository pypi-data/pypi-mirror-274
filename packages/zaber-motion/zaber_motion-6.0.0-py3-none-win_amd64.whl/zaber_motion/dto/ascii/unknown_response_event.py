# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .message_type import MessageType


@dataclass
class UnknownResponseEvent:
    """
    Reply that could not be matched to a request.
    """

    device_address: int
    """
    Number of the device that sent the message.
    """

    axis_number: int
    """
    Number of the axis which the response applies to. Zero denotes device scope.
    """

    reply_flag: str
    """
    The reply flag indicates if the request was accepted (OK) or rejected (RJ).
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

    message_type: MessageType
    """
    Type of the reply received.
    """

    @staticmethod
    def zero_values() -> 'UnknownResponseEvent':
        return UnknownResponseEvent(
            device_address=0,
            axis_number=0,
            reply_flag="",
            status="",
            warning_flag="",
            data="",
            message_type=next(first for first in MessageType),
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'UnknownResponseEvent':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return UnknownResponseEvent.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'deviceAddress': self.device_address,
            'axisNumber': self.axis_number,
            'replyFlag': self.reply_flag,
            'status': self.status,
            'warningFlag': self.warning_flag,
            'data': self.data,
            'messageType': self.message_type.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnknownResponseEvent':
        return UnknownResponseEvent(
            device_address=data.get('deviceAddress'),  # type: ignore
            axis_number=data.get('axisNumber'),  # type: ignore
            reply_flag=data.get('replyFlag'),  # type: ignore
            status=data.get('status'),  # type: ignore
            warning_flag=data.get('warningFlag'),  # type: ignore
            data=data.get('data'),  # type: ignore
            message_type=MessageType(data.get('messageType')),  # type: ignore
        )
