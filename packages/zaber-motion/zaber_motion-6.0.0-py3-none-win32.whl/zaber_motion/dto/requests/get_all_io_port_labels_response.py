# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.io_port_label import IoPortLabel


@dataclass
class GetAllIoPortLabelsResponse:

    labels: List[IoPortLabel] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'GetAllIoPortLabelsResponse':
        return GetAllIoPortLabelsResponse(
            labels=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetAllIoPortLabelsResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetAllIoPortLabelsResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'labels': [item.to_dict() for item in self.labels],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetAllIoPortLabelsResponse':
        return GetAllIoPortLabelsResponse(
            labels=[IoPortLabel.from_dict(item) for item in data.get('labels')],  # type: ignore
        )
