import sys

from mlflow.dto.runs_dto import ParamDto
from mlflow.entities._mlflow_object import _MLflowObject


class Param(_MLflowObject):
    """
    Parameter object.
    """

    def __init__(self, key, value):
        if "pyspark.ml" in sys.modules:
            import pyspark.ml.param

            if isinstance(key, pyspark.ml.param.Param):
                key = key.name
                value = str(value)
        self._key = key
        self._value = value

    @property
    def key(self):
        """String key corresponding to the parameter name."""
        return self._key

    @property
    def value(self):
        """String value of the parameter."""
        return self._value

    @classmethod
    def from_dto(cls, dto):
        return cls(dto.key, dto.value)

    def to_dto(self) -> ParamDto:
        return ParamDto(key=self.key, value=self.value)
