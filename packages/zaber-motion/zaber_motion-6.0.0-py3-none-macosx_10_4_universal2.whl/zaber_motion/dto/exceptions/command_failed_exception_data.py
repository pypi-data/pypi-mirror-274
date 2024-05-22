# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class CommandFailedExceptionData:
    """
    Contains additional data for CommandFailedException.
    """

    command: str
    """
    The command that got rejected.
    """

    response_data: str
    """
    The data from the reply containing the rejection reason.
    """

    reply_flag: str
    """
    The flag indicating that the command was rejected.
    """

    status: str
    """
    The current device or axis status.
    """

    warning_flag: str
    """
    The highest priority warning flag on the device or axis.
    """

    device_address: int
    """
    The address of the device that rejected the command.
    """

    axis_number: int
    """
    The number of the axis which the rejection relates to.
    """

    id: int
    """
    The message ID of the reply.
    """

    @staticmethod
    def zero_values() -> 'CommandFailedExceptionData':
        return CommandFailedExceptionData(
            command="",
            response_data="",
            reply_flag="",
            status="",
            warning_flag="",
            device_address=0,
            axis_number=0,
            id=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'CommandFailedExceptionData':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return CommandFailedExceptionData.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'command': self.command,
            'responseData': self.response_data,
            'replyFlag': self.reply_flag,
            'status': self.status,
            'warningFlag': self.warning_flag,
            'deviceAddress': self.device_address,
            'axisNumber': self.axis_number,
            'id': self.id,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CommandFailedExceptionData':
        return CommandFailedExceptionData(
            command=data.get('command'),  # type: ignore
            response_data=data.get('responseData'),  # type: ignore
            reply_flag=data.get('replyFlag'),  # type: ignore
            status=data.get('status'),  # type: ignore
            warning_flag=data.get('warningFlag'),  # type: ignore
            device_address=data.get('deviceAddress'),  # type: ignore
            axis_number=data.get('axisNumber'),  # type: ignore
            id=data.get('id'),  # type: ignore
        )
