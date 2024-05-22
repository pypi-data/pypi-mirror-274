# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from ..ascii.simple_tuning_param_definition import SimpleTuningParamDefinition


@dataclass
class GetSimpleTuningParamDefinitionResponse:

    params: List[SimpleTuningParamDefinition] = field(default_factory=list)

    @staticmethod
    def zero_values() -> 'GetSimpleTuningParamDefinitionResponse':
        return GetSimpleTuningParamDefinitionResponse(
            params=[],
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'GetSimpleTuningParamDefinitionResponse':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return GetSimpleTuningParamDefinitionResponse.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'params': [item.to_dict() for item in self.params],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'GetSimpleTuningParamDefinitionResponse':
        return GetSimpleTuningParamDefinitionResponse(
            params=[SimpleTuningParamDefinition.from_dict(item) for item in data.get('params')],  # type: ignore
        )
