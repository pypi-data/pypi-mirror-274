# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.io_port_type import IoPortType
from ..ascii.trigger_condition import TriggerCondition


@dataclass
class TriggerFireWhenIoRequest:

    interface_id: int = 0

    device: int = 0

    trigger_number: int = 0

    port_type: IoPortType = next(first for first in IoPortType)

    channel: int = 0

    trigger_condition: TriggerCondition = next(first for first in TriggerCondition)

    value: float = 0

    @staticmethod
    def zero_values() -> 'TriggerFireWhenIoRequest':
        return TriggerFireWhenIoRequest(
            interface_id=0,
            device=0,
            trigger_number=0,
            port_type=next(first for first in IoPortType),
            channel=0,
            trigger_condition=next(first for first in TriggerCondition),
            value=0,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TriggerFireWhenIoRequest':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TriggerFireWhenIoRequest.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'interfaceId': self.interface_id,
            'device': self.device,
            'triggerNumber': self.trigger_number,
            'portType': self.port_type.value,
            'channel': self.channel,
            'triggerCondition': self.trigger_condition.value,
            'value': self.value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TriggerFireWhenIoRequest':
        return TriggerFireWhenIoRequest(
            interface_id=data.get('interfaceId'),  # type: ignore
            device=data.get('device'),  # type: ignore
            trigger_number=data.get('triggerNumber'),  # type: ignore
            port_type=IoPortType(data.get('portType')),  # type: ignore
            channel=data.get('channel'),  # type: ignore
            trigger_condition=TriggerCondition(data.get('triggerCondition')),  # type: ignore
            value=data.get('value'),  # type: ignore
        )
