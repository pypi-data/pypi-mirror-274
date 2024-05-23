import typing

from mlflow.dto.artifacts_dto import *
from mlflow.dto.auth_dto import *
from mlflow.dto.experiments_dto import *
from mlflow.dto.metrics_dto import *
from mlflow.dto.mlfoundry_artifacts_dto import *
from mlflow.dto.python_deployment_config_dto import *
from mlflow.dto.runs_dto import *
from mlflow.entities.mlfoundry_artifacts.enums import ArtifactType


class Openapi:
    path = "/openapi.json"
    method = "HEAD"
    response_dto = None
    request_dto = {"return": "JSONResponse", "req": "Request"}


class SwaggerUiHtml:
    path = "/docs"
    method = "HEAD"
    response_dto = None
    request_dto = {"return": "HTMLResponse", "req": "Request"}


class SwaggerUiRedirect:
    path = "/docs/oauth2-redirect"
    method = "HEAD"
    response_dto = None
    request_dto = {"return": "HTMLResponse", "req": "Request"}


class RedocHtml:
    path = "/redoc"
    method = "HEAD"
    response_dto = None
    request_dto = {"return": "HTMLResponse", "req": "Request"}


class ListModel:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/models/list"
    method = "POST"
    response_dto = ListModelsResponseDto
    request_dto = ListModelsRequestDto


class GetModel:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/models/get"
    method = "GET"
    response_dto = ModelResponseDto
    request_dto = {"id": "str"}


class GetModelUsingFqn:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/models/get-by-fqn"
    method = "GET"
    response_dto = ModelResponseDto
    request_dto = {"fqn": "str"}


class GetModelUsingName:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/models/get-by-name"
    method = "GET"
    response_dto = ModelResponseDto
    request_dto = {"experiment_id": "int", "name": "str"}


class CreateModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/create"
    method = "POST"
    response_dto = ModelVersionResponseDto
    request_dto = CreateModelVersionRequestDto


class AuthorizeUserForModel:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/models/authorize"
    method = "POST"
    response_dto = None
    request_dto = AuthorizeUserForModelRequestDto


class AddCustomMetricsToModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/custom-metrics/add"
    method = "POST"
    response_dto = ModelVersionResponseDto
    request_dto = AddCustomMetricsToModelVersionRequestDto


class DeleteModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/delete"
    method = "POST"
    response_dto = None
    request_dto = DeleteModelVersionRequestDto


class AuthorizeUserForModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/authorize"
    method = "POST"
    response_dto = None
    request_dto = AuthorizeUserForModelVersionRequestDto


class AddFeaturesToModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/features/add"
    method = "POST"
    response_dto = ModelVersionResponseDto
    request_dto = AddFeaturesToModelVersionRequestDto


class GetModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/get"
    method = "GET"
    response_dto = ModelVersionResponseDto
    request_dto = {"id": "str"}


class GetModelVersionByName:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/get-by-name"
    method = "GET"
    response_dto = ModelVersionResponseDto
    request_dto = {"name": "str", "experiment_id": "int", "version": typing.Optional[int]}


class GetModelVersionByFqn:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/get-by-fqn"
    method = "GET"
    response_dto = ModelVersionResponseDto
    request_dto = {"fqn": "str"}


class ListModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/list"
    method = "POST"
    response_dto = ListModelVersionResponseDto
    request_dto = ListModelVersionsRequestDto


class UpdateModelVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/model-versions/update"
    method = "POST"
    response_dto = ModelVersionResponseDto
    request_dto = UpdateModelVersionRequestDto


class GetArtifactById:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifacts/get"
    method = "GET"
    response_dto = ArtifactResponseDto
    request_dto = {"id": "str"}


class GetArtifactByFqn:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifacts/get-by-fqn"
    method = "GET"
    response_dto = ArtifactResponseDto
    request_dto = {"fqn": "str"}


class DeleteArtifact:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact/delete"
    method = "POST"
    response_dto = None
    request_dto = DeleteModelVersionRequestDto


class CreateArtifact:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifacts/create"
    method = "POST"
    response_dto = CreateArtifactResponseDto
    request_dto = CreateArtifactRequestDto


class ListArtifacts:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifacts/list"
    method = "POST"
    response_dto = ListArtifactsResponseDto
    request_dto = ListArtifactsRequestDto


class CreateArtifactVersions:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/create"
    method = "POST"
    response_dto = CreateArtifactVersionResponseDto
    request_dto = CreateArtifactVersionRequestDto


class DeleteArtifactVersions:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/delete"
    method = "POST"
    response_dto = None
    request_dto = DeleteArtifactVersionsRequestDto


class ListFilesForArtifactVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/files/list"
    method = "POST"
    response_dto = ListFilesForArtifactVersionsResponseDto
    request_dto = ListFilesForArtifactVersionRequestDto


class FinalizeArtifactVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/finalize"
    method = "POST"
    response_dto = ArtifactVersionResponseDto
    request_dto = FinalizeArtifactVersionRequestDto


class GetArtifactVersionById:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/get"
    method = "GET"
    response_dto = ArtifactVersionResponseDto
    request_dto = {"id": "str"}


class GetArtifactVersionByFqn:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/get-by-fqn"
    method = "GET"
    response_dto = ArtifactVersionResponseDto
    request_dto = {"fqn": "str"}


class GetArtifactVersionByName:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/get-by-name"
    method = "GET"
    response_dto = ArtifactVersionResponseDto
    request_dto = {
        "experiment_id": "int",
        "artifact_name": "str",
        "version": typing.Optional[int],
        "artifact_type": typing.Optional[ArtifactType],
    }


class GetSignedUrlsForRead:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/get-signed-urls-for-read"
    method = "POST"
    response_dto = GetSignedURLsForArtifactVersionReadResponseDto
    request_dto = GetSignedURLsForArtifactVersionReadRequestDto


class GetSignedUrlsForWrite:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/get-signed-urls-for-write"
    method = "POST"
    response_dto = GetSignedURLsForArtifactVersionWriteResponseDto
    request_dto = GetSignedURLsForArtifactVersionWriteRequestDto


class ListArtifactVersions:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/list"
    method = "POST"
    response_dto = ListArtifactVersionsResponseDto
    request_dto = ListArtifactVersionsRequestDto


class NotifyFailure:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/notify-failure"
    method = "POST"
    response_dto = None
    request_dto = NotifyArtifactVersionFailureDto


class UpdateArtifactVersions:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/update"
    method = "POST"
    response_dto = ArtifactVersionResponseDto
    request_dto = UpdateArtifactVersionRequestDto


class FinalizeArtifactVersion:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/finalize"
    method = "POST"
    response_dto = ArtifactVersionResponseDto
    request_dto = FinalizeArtifactVersionRequestDto


class CreateDataset:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/create"
    method = "POST"
    response_dto = DatasetResponseDto
    request_dto = CreateDatasetRequestDto


class GetDataset:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/get"
    method = "GET"
    response_dto = DatasetResponseDto
    request_dto = {"id": "str"}


class GetDatasetByFqn:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/get-by-fqn"
    method = "GET"
    response_dto = DatasetResponseDto
    request_dto = {"fqn": "str"}


class GetSignedUrlsDatasetRead:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/get-signed-urls-for-read"
    method = "POST"
    response_dto = GetSignedURLsForDatasetReadResponseDto
    request_dto = GetSignedURLsForDatasetReadRequestDto


class GetSignedUrlsForDatasetWrite:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/get-signed-urls-for-write"
    method = "GET"
    response_dto = GetSignedURLsForDatasetWriteResponseDto
    request_dto = {"paths": typing.List[str], "dataset_fqn": "str"}


class ListFilesForDataset:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/files/list"
    method = "POST"
    response_dto = ListFilesForDatasetResponseDto
    request_dto = ListFilesForDatasetRequestDto


class CreateMultipartUploadForDataset:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/multi-part-upload/create"
    method = "POST"
    response_dto = CreateMultiPartUploadForDatasetResponseDto
    request_dto = CreateMultiPartUploadForDatasetRequestDto


class ListDatasets:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/list"
    method = "POST"
    response_dto = ListDatasetsResponseDto
    request_dto = ListDatasetsRequestDto


class UpdateDataset:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/datasets/update"
    method = "POST"
    response_dto = DatasetResponseDto
    request_dto = UpdateDatasetRequestDto


class CreateMultiPartUpload:
    path = "/api/2.0/mlflow/mlfoundry-artifacts/artifact-versions/multi-part-upload/create"
    method = "POST"
    response_dto = MultiPartUploadResponseDto
    request_dto = CreateMultiPartUploadRequestDto


class CreateRun:
    path = "/api/2.0/mlflow/runs/create"
    method = "POST"
    response_dto = CreateRunResponseDto
    request_dto = CreateRunRequestDto


class DeleteRun:
    path = "/api/2.0/mlflow/runs/delete"
    method = "POST"
    response_dto = None
    request_dto = DeleteRunRequest


class HardDeleteRun:
    path = "/api/2.0/mlflow/runs/hard-delete"
    method = "POST"
    response_dto = None
    request_dto = DeleteRunRequest


class UpdateRun:
    path = "/api/2.0/mlflow/runs/update"
    method = "POST"
    response_dto = UpdateRunResponseDto
    request_dto = UpdateRunRequestDto


class RestoreRun:
    path = "/api/2.0/mlflow/runs/restore"
    method = "POST"
    response_dto = None
    request_dto = RestoreRunRequestDto


class LogMetric:
    path = "/api/2.0/mlflow/runs/log-metric"
    method = "POST"
    response_dto = None
    request_dto = LogMetricRequestDto


class RunLogs:
    path = "/api/2.0/mlflow/runs/run-logs"
    method = "POST"
    response_dto = None
    request_dto = StoreRunLogsRequestDto


class LogParameter:
    path = "/api/2.0/mlflow/runs/log-parameter"
    method = "POST"
    response_dto = None
    request_dto = LogParamRequestDto


class LatestRunLog:
    path = "/api/2.0/mlflow/runs/run-logs/latest-run-log"
    method = "GET"
    response_dto = GetLatestRunLogResponseDto
    request_dto = {"run_uuid": "str", "key": "str", "log_type": "str"}


class ListRunLogs:
    path = "/api/2.0/mlflow/runs/run-logs/list"
    method = "GET"
    response_dto = ListRunLogsResponseDto
    request_dto = {
        "run_uuid": "str",
        "key": typing.Optional[str],
        "log_type": typing.Optional[str],
        "steps": typing.Optional[typing.List[int]],
    }


class ListLatestRunLogs:
    path = "/api/2.0/mlflow/runs/run-logs/list-latest"
    method = "GET"
    response_dto = ListLatestRunLogsResponseDto
    request_dto = {"run_uuid": "str", "key": typing.Optional[str], "log_type": typing.Optional[str]}


class SetTag:
    path = "/api/2.0/mlflow/runs/set-tag"
    method = "POST"
    response_dto = None
    request_dto = SetTagRequestDto


class DeleteTag:
    path = "/api/2.0/mlflow/runs/delete-tag"
    method = "POST"
    response_dto = None
    request_dto = DeleteTagRequestDto


class GetRun:
    path = "/api/2.0/mlflow/runs/get"
    method = "GET"
    response_dto = RunResponseDto
    request_dto = {"run_id": typing.Optional[str], "run_uuid": typing.Optional[str]}


class GetRunByFqn:
    path = "/api/2.0/mlflow/runs/get-by-fqn"
    method = "GET"
    response_dto = RunResponseDto
    request_dto = {"run_fqn": "str"}


class SearchRuns:
    path = "/api/2.0/mlflow/runs/search"
    method = "POST"
    response_dto = SearchRunsResponseDto
    request_dto = SearchRunsRequestDto


class GetRunByName:
    path = "/api/2.0/mlflow/runs/get-by-name"
    method = "GET"
    response_dto = RunResponseDto
    request_dto = {
        "run_name": "str",
        "experiment_id": typing.Optional[str],
        "experiment_name": typing.Optional[str],
    }


class LogRunBatch:
    path = "/api/2.0/mlflow/runs/log-batch"
    method = "POST"
    response_dto = None
    request_dto = LogBatchRequestDto


class LogModel:
    path = "/api/2.0/mlflow/runs/log-model"
    method = "POST"
    response_dto = None
    request_dto = LogModelRequestDto


class GetExperimentByName:
    path = "/api/2.0/mlflow/experiments/get-by-name"
    method = "GET"
    response_dto = ExperimentResponseDto
    request_dto = {"experiment_name": "str"}


class CreateExperiment:
    path = "/api/2.0/mlflow/experiments/create"
    method = "POST"
    response_dto = CreateExperimentResponseDto
    request_dto = CreateExperimentRequestDto


class ListExperiment:
    path = "/api/2.0/mlflow/experiments/list"
    method = "GET"
    response_dto = ListExperimentsResponseDto
    request_dto = {
        "view_type": typing.Optional[int],
        "max_results": typing.Optional[int],
        "page_token": typing.Optional[str],
        "privacy_type": typing.Optional[str],
        "offset": typing.Optional[int],
        "filter_name": typing.Optional[str],
    }


class SeedListExperiment:
    path = "/api/2.0/mlflow/experiments/seed/list"
    method = "GET"
    response_dto = ListSeedExperimentsResponseDto
    request_dto = {}


class GetExperiment:
    path = "/api/2.0/mlflow/experiments/get"
    method = "GET"
    response_dto = GetExperimentResponseDto
    request_dto = {"experiment_id": "str"}


class DeleteExperiment:
    path = "/api/2.0/mlflow/experiments/delete"
    method = "POST"
    response_dto = None
    request_dto = ExperimentIdRequestDto


class HardDeleteExperiment:
    path = "/api/2.0/mlflow/experiments/hard-delete"
    method = "POST"
    response_dto = None
    request_dto = ExperimentIdRequestDto


class RestoreExperiment:
    path = "/api/2.0/mlflow/experiments/restore"
    method = "POST"
    response_dto = None
    request_dto = ExperimentIdRequestDto


class SetExperimentTag:
    path = "/api/2.0/mlflow/experiments/set-experiment-tag"
    method = "POST"
    response_dto = None
    request_dto = SetExperimentTagRequestDto


class UpdateExperiment:
    path = "/api/2.0/mlflow/experiments/update"
    method = "POST"
    response_dto = None
    request_dto = UpdateExperimentRequestDto


class BackfillStorageIntegration:
    path = "/api/2.0/mlflow/experiments/storage-integration/backfill"
    method = "POST"
    response_dto = None
    request_dto = BackfillDefaultStorageIntegrationIdRequestDto


class ListExperimentColumns:
    path = "/api/2.0/mlflow/experiments/columns"
    method = "GET"
    response_dto = None
    request_dto = {"experiment_id": "str"}


class PutPrivacyType:
    path = "/api/2.0/mlflow/experiments/privacy-type"
    method = "PUT"
    response_dto = None
    request_dto = SetExperimentTagRequestDto


class GetMetricHistory:
    path = "/api/2.0/mlflow/metrics/get-history"
    method = "GET"
    response_dto = GetMetricHistoryResponse
    request_dto = {
        "run_uuid": typing.Optional[str],
        "run_id": typing.Optional[str],
        "metric_key": typing.Optional[str],
    }


class ListMetricHistory:
    path = "/api/2.0/mlflow/metrics/list-history"
    method = "POST"
    response_dto = ListMetricHistoryResponseDto
    request_dto = ListMetricHistoryRequestDto


class GeneratePyDevelopmentConfig:
    path = "/api/2.0/mlflow/python-deployment-config/generate"
    method = "POST"
    response_dto = CreatePythonDeploymentConfigResponseDto
    request_dto = CreatePythonDeploymentConfigRequestDto


class GetTenantId:
    path = "/api/2.0/mlflow/tenant-id"
    method = "GET"
    response_dto = GetTenantIdResponseDto
    request_dto = {"host_name": "str"}


class Serve:
    path = "/"
    method = "GET"
    response_dto = None
    request_dto = {"request": "Request"}


class Health:
    path = "/health"
    method = "GET"
    response_dto = None
    request_dto = {}
