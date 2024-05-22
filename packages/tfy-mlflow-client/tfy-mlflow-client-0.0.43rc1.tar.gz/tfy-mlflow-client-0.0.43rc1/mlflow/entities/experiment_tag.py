from mlflow.dto.experiments_dto import ExperimentTagDto as ExperimentTagDto
from mlflow.entities._mlflow_object import _MLflowObject


class ExperimentTag(_MLflowObject):
    """Tag object associated with an experiment."""

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def key(self):
        """String name of the tag."""
        return self._key

    @property
    def value(self):
        """String value of the tag."""
        return self._value

    def to_dto(self) -> ExperimentTagDto:
        return ExperimentTagDto(key=self.key, value=self.value)

    @classmethod
    def from_dto(cls, dto):
        return cls(key=dto.key, value=dto.value)
