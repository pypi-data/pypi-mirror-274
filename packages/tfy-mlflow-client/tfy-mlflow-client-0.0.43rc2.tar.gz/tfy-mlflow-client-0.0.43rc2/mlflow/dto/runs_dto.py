from typing import List, Optional

from mlflow.dto.metrics_dto import MetricDto
from mlflow.pydantic_v1 import BaseModel, ValidationError, root_validator


class RunInfoDto(BaseModel):
    run_uuid: Optional[str]
    run_id: Optional[str]
    experiment_id: Optional[str]
    user_id: Optional[str]
    status: Optional[str]
    start_time: Optional[int]
    end_time: Optional[int]
    artifact_uri: Optional[str]
    lifecycle_stage: Optional[str]
    name: Optional[str]
    fqn: Optional[str]
    description: Optional[str]


class RunTagDto(BaseModel):
    key: str
    value: str


class ParamDto(BaseModel):
    key: str
    value: str


class RunDataDto(BaseModel):
    metrics: Optional[List[MetricDto]]
    params: Optional[List[ParamDto]]
    tags: Optional[List[RunTagDto]]


class RunDto(BaseModel):
    info: RunInfoDto
    data: Optional[RunDataDto]


class RunLogDto(BaseModel):
    key: Optional[str]
    timestamp: Optional[int]
    step: Optional[int]
    log_type: Optional[str]
    artifact_path: Optional[str]
    value: Optional[str]
    artifact_signed_uri: Optional[str]


class RunLogInputDto(BaseModel):
    key: str  # Name of the log
    value: Optional[str]
    timestamp: int  # Unix timestamp in milliseconds at the time log was created
    step: Optional[int] = 0  # Step at which to log the input
    log_type: str  # Type of the log
    artifact_path: Optional[str]  # Path to the artifact if it's an artifact log


class LatestRunLogDto(BaseModel):
    run_log: Optional[RunLogDto]
    steps: List[int]


class RunResponseDto(BaseModel):
    run: RunDto


class CreateRunRequestDto(BaseModel):
    experiment_id: Optional[str]
    user_id: Optional[str]
    start_time: Optional[int]
    tags: Optional[List[RunTagDto]]
    name: Optional[str]
    description: Optional[str]


class CreateRunResponseDto(BaseModel):
    run: Optional[RunDto]


class UpdateRunRequestDto(BaseModel):
    run_id: Optional[str]
    run_uuid: Optional[str]
    status: Optional[str]
    end_time: Optional[int]
    description: Optional[str]

    @root_validator
    def check_run_id_or_run_uuid(cls, values):
        run_id, run_uuid = values.get("run_id"), values.get("run_uuid")
        if not run_id and not run_uuid:
            raise ValidationError("Either run_id or run_uuid must be provided")
        return values


class UpdateRunResponseDto(BaseModel):
    run_info: Optional[RunInfoDto]


class DeleteRunRequest(BaseModel):
    run_id: str


class RestoreRunRequestDto(BaseModel):
    run_id: str


class LogMetricRequestDto(BaseModel):
    run_id: Optional[str]
    run_uuid: Optional[str]  # Deprecated, use run_id instead
    key: str  # Name of the metric
    value: float  # Double value of the metric being logged
    timestamp: int  # Unix timestamp in milliseconds at the time metric was logged
    step: Optional[int] = 0  # Step at which to log the metric

    @root_validator
    def check_run_id_or_run_uuid(cls, values):
        run_id, run_uuid = values.get("run_id"), values.get("run_uuid")
        if not run_id and not run_uuid:
            raise ValidationError("Either run_id or run_uuid must be provided")
        return values


class StoreRunLogsRequestDto(BaseModel):
    run_uuid: str
    run_logs: List[RunLogInputDto]


class GetLatestRunLogResponseDto(BaseModel):
    run_log: Optional[RunLogDto]


class ListRunLogsResponseDto(BaseModel):
    run_logs: Optional[List[RunLogDto]]


class ListLatestRunLogsResponseDto(BaseModel):
    latest_run_logs: List[LatestRunLogDto]


class LogParamRequestDto(BaseModel):
    run_id: Optional[str]
    run_uuid: Optional[str]  # Deprecated, use run_id instead
    key: str  # Name of the param. Maximum size is 255 bytes.
    value: str  # String value of the param being logged. Maximum size is 500 bytes.

    @root_validator
    def check_run_id_or_run_uuid(cls, values):
        run_id, run_uuid = values.get("run_id"), values.get("run_uuid")
        if not run_id and not run_uuid:
            raise ValidationError("Either run_id or run_uuid must be provided")
        return values


class SetTagRequestDto(BaseModel):
    run_id: Optional[str]
    run_uuid: Optional[str]  # Deprecated, use run_id instead
    key: str  # Name of the tag
    value: str  # String value of the tag being logged

    @root_validator
    def check_run_id_or_run_uuid(cls, values):
        run_id, run_uuid = values.get("run_id"), values.get("run_uuid")
        if not run_id and not run_uuid:
            raise ValidationError("Either run_id or run_uuid must be provided")
        return values


class DeleteTagRequestDto(BaseModel):
    run_id: str  # ID of the run that the tag was logged under. Must be provided.
    key: str  # Name of the tag. Maximum size is 255 bytes. Must be provided.


class SearchRunsRequestDto(BaseModel):
    #   // List of experiment IDs to search over.
    experiment_ids: Optional[List[str]]

    #   // A filter expression over params, metrics, and tags, that allows returning a subset of
    #   // runs. The syntax is a subset of SQL that supports ANDing together binary operations
    #   // between a param, metric, or tag and a constant.
    #   //
    #   // Example: ``metrics.rmse < 1 and params.model_class = 'LogisticRegression'``
    #   //
    #   // You can select columns with special characters (hyphen, space, period, etc.) by using double quotes:
    #   // ``metrics."model class" = 'LinearRegression' and tags."user-name" = 'Tomas'``
    #   //
    #   // Supported operators are ``=``, ``!=``, ``>``, ``>=``, ``<``, and ``<=``.

    filter: Optional[str]
    #     // Whether to display only active, only deleted, or all runs.
    #   // Defaults to only active runs.
    run_view_type: Optional[str] = "ACTIVE_ONLY"

    #   // Maximum number of runs desired. If unspecified, defaults to 1000.
    #   // All servers are guaranteed to support a `max_results` threshold of at least 50,000
    #   // but may support more. Callers of this endpoint are encouraged to pass max_results
    #   // explicitly and leverage page_token to iterate through experiments.

    max_results: Optional[int] = 1000
    #       // List of columns to be ordered by, including attributes, params, metrics, and tags with an
    #   // optional "DESC" or "ASC" annotation, where "ASC" is the default.
    #   // Example: ["params.input DESC", "metrics.alpha ASC", "metrics.rmse"]
    #   // Tiebreaks are done by start_time DESC followed by run_id for runs with the same start time
    #   // (and this is the default ordering criterion if order_by is not provided).

    order_by: Optional[List[str]]
    page_token: Optional[str]
    offset: Optional[int] = None


class SearchRunsResponseDto(BaseModel):
    runs: List[RunDto]
    next_page_token: Optional[str]
    total: Optional[int]

    class Config:
        arbitrary_types_allowed = True


class LogBatchRequestDto(BaseModel):
    run_id: Optional[str]
    metrics: Optional[List[MetricDto]]
    params: Optional[List[ParamDto]]
    tags: Optional[List[RunTagDto]]


class LogModelRequestDto(BaseModel):
    run_id: Optional[str]
    model_json: Optional[str]
