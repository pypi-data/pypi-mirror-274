import typing
from operator import xor

from mlflow.dto.runs_dto import LatestRunLogDto, RunLogDto
from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE


class RunLog(_MLflowObject):
    """
    Run Log object.
    """

    def __init__(
        self,
        key,
        timestamp,
        step,
        log_type,
        artifact_path=None,
        value=None,
        artifact_signed_uri: typing.Optional[str] = None,
    ):
        if not xor(bool(artifact_path), bool(value)):
            raise MlflowException(
                "either artifact_path or value should be empty. "
                f"artifact_path={artifact_path}, value={value}",
                INVALID_PARAMETER_VALUE,
            )

        self._key = key
        self._value = value
        self._timestamp = timestamp
        self._step = step
        self._log_type = log_type
        self._artifact_path = artifact_path
        self._artifact_signed_uri = None
        self.set_artifact_signed_uri(artifact_signed_uri)

    def set_artifact_signed_uri(self, artifact_signed_uri: str):
        if artifact_signed_uri and not self.artifact_path:
            raise MlflowException("artifact_signed_uri cannot be set if artifact_path is not set")
        self._artifact_signed_uri = artifact_signed_uri

    @property
    def artifact_signed_uri(self) -> typing.Optional[str]:
        return self._artifact_signed_uri

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

    @property
    def log_type(self):
        """type of non scalar metric to log"""
        return self._log_type

    @property
    def artifact_path(self):
        """artifact_path of non scalar metric (can be none)"""
        return self._artifact_path

    def to_dto(self) -> RunLogDto:
        return RunLogDto(
            key=self.key,
            timestamp=self.timestamp,
            step=self.step,
            log_type=self.log_type,
            artifact_path=self.artifact_path,
            value=self.value,
            artifact_signed_uri=self.artifact_signed_uri,
        )

    @classmethod
    def from_dto(cls, dto):
        return cls(
            key=dto.key,
            timestamp=dto.timestamp,
            step=dto.step,
            log_type=dto.log_type,
            artifact_path=dto.artifact_path or None,
            value=dto.value or None,
            artifact_signed_uri=dto.artifact_signed_uri or None,
        )


class LatestRunLog:
    def __init__(self, run_log: RunLog, steps: typing.List[int]):
        self.run_log = run_log
        self.steps = steps

    def to_dto(self) -> LatestRunLogDto:
        return LatestRunLog(run_log=self.run_log.to_dto(), steps=self.steps)
