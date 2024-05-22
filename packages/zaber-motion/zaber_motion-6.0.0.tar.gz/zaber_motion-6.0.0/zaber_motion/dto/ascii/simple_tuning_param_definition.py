# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson


@dataclass
class SimpleTuningParamDefinition:
    """
    Information about a parameter used for the simple tuning method.
    """

    name: str
    """
    The name of the parameter.
    """

    min_label: str
    """
    The human readable description of the effect of a lower value on this setting.
    """

    max_label: str
    """
    The human readable description of the effect of a higher value on this setting.
    """

    data_type: str
    """
    How this parameter will be parsed by the tuner.
    """

    default_value: Optional[float] = None
    """
    The default value of this parameter.
    """

    @staticmethod
    def zero_values() -> 'SimpleTuningParamDefinition':
        return SimpleTuningParamDefinition(
            name="",
            min_label="",
            max_label="",
            data_type="",
            default_value=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'SimpleTuningParamDefinition':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return SimpleTuningParamDefinition.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'minLabel': self.min_label,
            'maxLabel': self.max_label,
            'dataType': self.data_type,
            'defaultValue': self.default_value,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SimpleTuningParamDefinition':
        return SimpleTuningParamDefinition(
            name=data.get('name'),  # type: ignore
            min_label=data.get('minLabel'),  # type: ignore
            max_label=data.get('maxLabel'),  # type: ignore
            data_type=data.get('dataType'),  # type: ignore
            default_value=data.get('defaultValue'),  # type: ignore
        )
