import typing

from mlflow.dto.experiments_dto import ColumnsDto


# "Columns", this name is too broad. Think whether this
# will collide with some other concept
class Columns:
    def __init__(
        self,
        metric_names: typing.Iterator[str],
        param_names: typing.Iterator[str],
        tag_names: typing.Iterator[str],
    ):
        self._metric_names = metric_names
        self._param_names = param_names
        self._tag_names = tag_names

    def to_dto(self) -> ColumnsDto:
        return ColumnsDto(
            metric_names=self._metric_names,
            param_names=self._param_names,
            tag_names=self._tag_names,
        )
