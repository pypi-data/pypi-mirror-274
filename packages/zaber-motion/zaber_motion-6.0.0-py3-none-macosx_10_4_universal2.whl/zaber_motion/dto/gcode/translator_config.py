# This file is generated. Do not modify by hand.
# pylint: disable=line-too-long, unused-argument, unused-import
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, TYPE_CHECKING
import bson
from .axis_mapping import AxisMapping
from .axis_transformation import AxisTransformation


@dataclass
class TranslatorConfig:
    """
    Configuration of a translator.
    """

    axis_mappings: Optional[List[AxisMapping]] = None
    """
    Optional custom mapping of translator axes to stream axes.
    """

    axis_transformations: Optional[List[AxisTransformation]] = None
    """
    Optional transformation of axes.
    """

    @staticmethod
    def zero_values() -> 'TranslatorConfig':
        return TranslatorConfig(
            axis_mappings=None,
            axis_transformations=None,
        )

    @staticmethod
    def from_binary(data_bytes: bytes) -> 'TranslatorConfig':
        """" Deserialize a binary representation of this class. """
        data = bson.loads(data_bytes)  # type: Dict[str, Any]
        return TranslatorConfig.from_dict(data)

    def to_binary(self) -> bytes:
        """" Serialize this class to a binary representation. """
        return bson.dumps(self.to_dict())  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        return {
            'axisMappings': [item.to_dict() for item in self.axis_mappings] if self.axis_mappings is not None else None,
            'axisTransformations': [item.to_dict() for item in self.axis_transformations] if self.axis_transformations is not None else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TranslatorConfig':
        return TranslatorConfig(
            axis_mappings=[AxisMapping.from_dict(item) for item in data.get('axisMappings')] if data.get('axisMappings') is not None else None,  # type: ignore
            axis_transformations=[AxisTransformation.from_dict(item) for item in data.get('axisTransformations')] if data.get('axisTransformations') is not None else None,  # type: ignore
        )
