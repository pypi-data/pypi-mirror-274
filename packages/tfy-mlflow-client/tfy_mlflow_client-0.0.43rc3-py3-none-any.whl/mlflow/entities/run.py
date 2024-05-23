from mlflow.dto.runs_dto import RunDto
from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.entities.run_data import RunData
from mlflow.entities.run_info import RunInfo
from mlflow.exceptions import MlflowException


class Run(_MLflowObject):
    """
    Run object.
    """

    def __init__(self, run_info, run_data):
        if run_info is None:
            raise MlflowException("run_info cannot be None")
        self._info = run_info
        self._data = run_data

    @property
    def info(self):
        """
        The run metadata, such as the run id, start time, and status.

        :rtype: :py:class:`mlflow.entities.RunInfo`
        """
        return self._info

    @property
    def data(self):
        """
        The run data, including metrics, parameters, and tags.

        :rtype: :py:class:`mlflow.entities.RunData`
        """
        return self._data

    def to_dictionary(self):
        run_dict = {
            "info": dict(self.info),
        }
        if self.data:
            run_dict["data"] = self.data.to_dictionary()
        return run_dict

    def to_dto(self) -> RunDto:
        return RunDto(
            info=self.info.to_dto(), data=self.data.to_dto() if self.data is not None else None
        )

    @classmethod
    def from_dto(cls, dto):
        return cls(run_info=RunInfo.from_dto(dto.info), run_data=RunData.from_dto(dto.data))
