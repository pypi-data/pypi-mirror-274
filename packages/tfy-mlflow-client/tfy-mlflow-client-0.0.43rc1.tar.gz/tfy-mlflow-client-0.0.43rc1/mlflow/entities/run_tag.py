from mlflow.dto.runs_dto import RunTagDto
from mlflow.entities._mlflow_object import _MLflowObject


class RunTag(_MLflowObject):
    """Tag object associated with a run."""

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __eq__(self, other):
        if type(other) is type(self):
            # TODO deep equality here?
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

    @classmethod
    def from_dto(cls, dto):
        return cls(dto.key, dto.value)

    def to_dto(self) -> RunTagDto:
        return RunTagDto(key=self.key, value=self.value)
