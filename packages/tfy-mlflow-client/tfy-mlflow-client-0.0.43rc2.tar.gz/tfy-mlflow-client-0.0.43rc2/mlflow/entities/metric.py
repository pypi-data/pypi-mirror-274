import math

from mlflow.dto.metrics_dto import MetricDto
from mlflow.entities._mlflow_object import _MLflowObject


class Metric(_MLflowObject):
    """
    Metric object.
    """

    def __init__(self, key, value, timestamp, step):
        self._key = key
        self._value = value
        self._timestamp = timestamp
        self._step = step

    @property
    def key(self):
        """String key corresponding to the metric name."""
        return self._key

    @property
    def value(self):
        """Float value of the metric."""
        return self._value

    @property
    def timestamp(self):
        """Metric timestamp as an integer (milliseconds since the Unix epoch)."""
        return self._timestamp

    @property
    def step(self):
        """Integer metric step (x-coordinate)."""
        return self._step

    @classmethod
    def from_dto(cls, dto):
        return cls(dto.key, dto.value, dto.timestamp, dto.step)

    def to_dto(self) -> MetricDto:
        return MetricDto(
            key=self.key,
            value=self.value,
            timestamp=self.timestamp,
            step=self.step,
        )
