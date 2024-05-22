# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.response import Response


@dataclass
class GenericCommandResponseCollection:

    responses: List[Response] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'GenericCommandResponseCollection':
        return GenericCommandResponseCollection(
            responses=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GenericCommandResponseCollection':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GenericCommandResponseCollection.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'responses': [item.to_dict() for item in self.responses],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GenericCommandResponseCollection':
        return GenericCommandResponseCollection(
            responses=[Response.from_dict(item) for item in data.get('responses')],  # type: ignore
        )
