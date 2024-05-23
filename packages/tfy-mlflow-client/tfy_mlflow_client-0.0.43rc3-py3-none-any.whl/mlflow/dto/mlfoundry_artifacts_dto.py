from datetime import datetime
from typing import Any, Dict, List, Optional

from mlflow.dto.experiments_dto import ExperimentDto
from mlflow.dto.metrics_dto import MetricDto
from mlflow.entities.mlfoundry_artifacts.enums import (
    ArtifactType,
    ArtifactVersionStatus,
    FeatureValueType,
    MultiPartUploadStorageProvider,
    PredictionType,
)
from mlflow.entities.sentinel import SENTINEL
from mlflow.pydantic_v1 import BaseModel, Field


class FeatureDto(BaseModel):
    name: Optional[str]
    type: Optional[FeatureValueType]


class ModelSchemaDto(BaseModel):
    features: Optional[List[FeatureDto]]
    prediction: Optional[PredictionType]


class SignedURLDto(BaseModel):
    signed_url: str
    path: Optional[str]


class ModelVersionDto(BaseModel):
    id: Optional[str]
    model_id: Optional[str]
    version: Optional[int]
    fqn: Optional[str]
    artifact_storage_root: Optional[str]
    artifact_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    description: Optional[str] = None
    status: Optional[ArtifactVersionStatus]
    step: Optional[int] = 0
    created_by: Optional[str]
    model_schema: Optional[ModelSchemaDto] = None
    custom_metrics: Optional[List[Dict[str, Any]]]
    created_at: Optional[str]
    updated_at: Optional[str]
    model_fqn: Optional[str]
    data_path: Optional[str] = None
    monitoring_enabled: Optional[bool] = False
    usage_code_snippet: Optional[str]
    experiment_id: Optional[str]
    run_id: Optional[str] = None
    metrics: Optional[List[MetricDto]]
    model_name: Optional[str]
    model_framework: Optional[str]
    artifact_size: Optional[int]


class ModelDto(BaseModel):
    id: Optional[str]
    experiment_id: Optional[str]
    type: Optional[ArtifactType]
    name: Optional[str]
    fqn: Optional[str]
    description: Optional[str] = None
    created_by: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    artifact_storage_root: Optional[str]
    latest_version: Optional[ModelVersionDto] = None
    monitoring_enabled: Optional[bool]
    experiment: Optional[ExperimentDto]


class DatasetDto(BaseModel):
    id: Optional[str]
    experiment_id: Optional[str]
    experiment: Optional[ExperimentDto]
    name: Optional[str]
    fqn: Optional[str]
    description: Optional[str] = None
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    storage_root: Optional[str]
    dataset_metadata: Optional[Dict] = Field(default_factory=dict)
    usage_code_snippet: Optional[str]


class ArtifactVersionDto(BaseModel):
    id: Optional[str]
    artifact_id: Optional[str]
    version: Optional[int]
    fqn: Optional[str]
    artifact_storage_root: Optional[str]
    artifact_metadata: Optional[Dict] = Field(default_factory=dict)
    description: Optional[str] = None
    status: Optional[ArtifactVersionStatus]
    step: Optional[int] = 0
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    artifact_fqn: Optional[str]
    data_path: Optional[str] = None
    usage_code_snippet: Optional[str]
    experiment_id: Optional[str]
    run_id: Optional[str] = None
    artifact_name: Optional[str]
    internal_metadata: Optional[Dict] = Field(default_factory=dict)
    artifact_size: Optional[int]


class ArtifactDto(BaseModel):
    id: Optional[str]
    experiment_id: Optional[str]
    type: Optional[ArtifactType]
    name: Optional[str]
    fqn: Optional[str]
    description: Optional[str] = None
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    artifact_storage_root: Optional[str]
    latest_version: Optional[ArtifactVersionDto] = None
    run_steps: Optional[List[int]]


class FileInfoDto(BaseModel):
    path: str
    is_dir: bool
    file_size: Optional[int]
    signed_url: Optional[str]


class MultiPartUploadDto(BaseModel):
    storage_provider: MultiPartUploadStorageProvider
    part_signed_urls: List[SignedURLDto]
    s3_compatible_upload_id: Optional[str]
    azure_blob_block_ids: Optional[List[str]]
    finalize_signed_url: SignedURLDto


class ListModelsRequestDto(BaseModel):
    experiment_id: Optional[str] = None
    name: Optional[str] = None
    max_results: Optional[int] = None
    offset: Optional[int] = None
    page_token: Optional[str] = None
    monitoring_enabled_only: Optional[bool] = False


class ListModelsResponseDto(BaseModel):
    models: List[ModelDto]
    next_page_token: Optional[str]
    total: Optional[int]


class ModelResponseDto(BaseModel):
    model: ModelDto


class ArtifactResponseDto(BaseModel):
    artifact: ArtifactDto


class AuthorizeUserForModelRequestDto(BaseModel):
    id: str
    role: Optional[str]


class CreateModelVersionRequestDto(BaseModel):
    artifact_version_id: str
    description: Optional[str] = Field(default_factory=lambda: SENTINEL)
    artifact_metadata: Dict[str, Any] = Field(default_factory=lambda: SENTINEL)
    data_path: Optional[str] = Field(default_factory=lambda: SENTINEL)
    step: Optional[int] = Field(default_factory=lambda: SENTINEL)
    internal_metadata: Dict[str, Any] = Field(default_factory=lambda: SENTINEL)


class GetModelVersionByNameRequestDto(BaseModel):
    name: str
    experiment_id: int
    version: Optional[int] = -1


class AuthorizeUserForModelVersionRequestDto(BaseModel):
    id: Optional[str]
    role: Optional[str]


class ListModelVersionsRequestDto(BaseModel):
    model_id: Optional[str]
    statuses: Optional[List[ArtifactVersionStatus]]
    max_results: Optional[int] = None
    offset: Optional[int] = None
    page_token: Optional[str] = None
    monitoring_enabled: Optional[bool] = None
    run_ids: Optional[List[str]]


class ListModelVersionResponseDto(BaseModel):
    model_versions: List[ModelVersionDto]
    next_page_token: Optional[str]
    total: Optional[int]


class UpdateModelVersionRequestDto(BaseModel):
    id: str
    description: Optional[str] = Field(default_factory=lambda: SENTINEL)
    artifact_metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: SENTINEL)
    model_schema: Optional[ModelSchemaDto] = Field(default_factory=lambda: SENTINEL)
    monitoring_enabled: Optional[bool] = Field(default_factory=lambda: SENTINEL)
    model_framework: Optional[str] = None


class AddFeaturesToModelVersionRequestDto(BaseModel):
    id: str
    features: List[FeatureDto]


class AddCustomMetricsToModelVersionRequestDto(BaseModel):
    id: str
    custom_metrics: List[Dict] = Field(default_factory=list)


class DeleteModelVersionRequestDto(BaseModel):
    id: str


class CreateArtifactRequestDto(BaseModel):
    experiment_id: str
    name: str
    artifact_type: ArtifactType


class CreateArtifactResponseDto(BaseModel):
    id: Optional[str]


class ModelVersionResponseDto(BaseModel):
    model_version: ModelVersionDto


class CreateDatasetRequestDto(BaseModel):
    name: str
    description: Optional[str]
    experiment_id: Optional[str]
    dataset_metadata: Optional[Dict]


class DatasetResponseDto(BaseModel):
    dataset: DatasetDto


class GetSignedURLsForDatasetReadRequestDto(BaseModel):
    dataset_fqn: str
    paths: List[str]


class ListFilesForDatasetRequestDto(BaseModel):
    dataset_fqn: str
    path: Optional[str] = None
    max_results: Optional[int] = None
    page_token: Optional[str] = None


class MultiPartUploadRequestDto(BaseModel):
    storage_provider: Optional[str]
    part_signed_urls: List[SignedURLDto]
    s3_compatible_upload_id: Optional[str]
    azure_blob_block_ids: Optional[List[str]]
    finalize_signed_url: Optional[SignedURLDto]


class MultiPartUploadResponseDto(BaseModel):
    multipart_upload: MultiPartUploadDto


class CreateMultiPartUploadRequestDto(BaseModel):
    artifact_version_id: str
    path: str
    num_parts: int


class CreateMultiPartUploadForDatasetRequestDto(BaseModel):
    dataset_fqn: str
    path: str
    num_parts: int


class UpdateDatasetRequestDto(BaseModel):
    fqn: str
    description: Optional[str] = Field(default_factory=lambda: SENTINEL)
    dataset_metadata: Optional[Dict] = Field(default_factory=lambda: SENTINEL)


class DeleteArtifactRequestDto(BaseModel):
    id: str


class ListArtifactsRequestDto(BaseModel):
    experiment_id: Optional[str] = None
    artifact_types: Optional[List[ArtifactType]]
    name: Optional[str] = None
    max_results: Optional[int]
    offset: Optional[int] = None
    page_token: Optional[str] = None
    run_id: Optional[str] = None
    include_models: Optional[bool] = False


class ListArtifactsResponseDto(BaseModel):
    artifacts: List[ArtifactDto]
    next_page_token: Optional[str]
    total: Optional[int]


class CreateArtifactVersionsRequestDto(BaseModel):
    experiment_id: Optional[str]
    name: Optional[str]
    artifact_type: Optional[ArtifactType]


class DeleteArtifactVersionsRequestDto(BaseModel):
    id: str


class ListFilesForArtifactVersionRequestDto(BaseModel):
    id: str
    path: Optional[str]
    max_results: Optional[int]
    page_token: Optional[str]


class ListFilesForArtifactVersionsResponseDto(BaseModel):
    files: List[FileInfoDto]
    next_page_token: Optional[str]


class FinalizeArtifactVersionRequestDto(BaseModel):
    id: str
    run_uuid: Optional[str]
    description: Optional[str] = None
    artifact_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    data_path: Optional[str] = None
    step: Optional[int] = None
    artifact_size: Optional[int] = None


class GetSignedURLsForArtifactVersionReadRequestDto(BaseModel):
    id: str
    paths: List[str]


class GetSignedURLsForArtifactVersionReadResponseDto(BaseModel):
    signed_urls: List[SignedURLDto]


class GetSignedURLsForArtifactVersionWriteRequestDto(BaseModel):
    id: str
    paths: Optional[List[str]]


class GetSignedURLsForArtifactVersionWriteResponseDto(BaseModel):
    signed_urls: List[SignedURLDto]


class ListArtifactVersionsRequestDto(BaseModel):
    artifact_id: Optional[str] = None
    statuses: Optional[List[ArtifactVersionStatus]]
    max_results: Optional[int] = None
    offset: Optional[int] = None
    page_token: Optional[str] = None
    run_ids: Optional[List[str]]
    artifact_types: Optional[List[ArtifactType]]
    run_steps: Optional[List[int]]
    include_internal_metadata: Optional[bool] = False
    include_model_versions: Optional[bool] = False


class ArtifactVersionResponseDto(BaseModel):
    artifact_version: ArtifactVersionDto


class ListArtifactVersionsResponseDto(BaseModel):
    artifact_versions: List[ArtifactVersionDto]
    next_page_token: Optional[str]
    total: Optional[int]


class NotifyArtifactVersionFailureDto(BaseModel):
    id: str


class UpdateArtifactVersionRequestDto(BaseModel):
    id: str
    description: Optional[str] = Field(default_factory=lambda: SENTINEL)
    artifact_metadata: Optional[Dict[str, Any]] = Field(default_factory=lambda: SENTINEL)


class FinalizeArtifactVersionRequestDto(BaseModel):
    id: str
    run_uuid: Optional[str]
    description: Optional[str]
    artifact_metadata: Optional[Dict[str, Any]]
    data_path: Optional[str]
    step: Optional[int]
    artifact_size: Optional[int]


class CreateArtifactVersionRequestDto(BaseModel):
    experiment_id: int
    name: str
    artifact_type: ArtifactType


class CreateArtifactVersionResponseDto(BaseModel):
    id: Optional[str]


class CreateDatasetRequestDto(BaseModel):
    name: str
    description: Optional[str] = None
    experiment_id: Optional[str]
    dataset_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class GetSignedURLForDatasetWriteRequestDto(BaseModel):
    dataset_fqn: str
    paths: List[str]


class GetSignedURLsForDatasetWriteResponseDto(BaseModel):
    signed_urls: List[SignedURLDto]


class GetSignedURLsForDatasetReadResponseDto(BaseModel):
    signed_urls: List[SignedURLDto]


class ListFilesForDatasetResponseDto(BaseModel):
    files: List[FileInfoDto]
    next_page_token: Optional[str]


class CreateMultiPartUploadForDatasetRequestDto(BaseModel):
    dataset_fqn: str
    path: str
    num_parts: int


class CreateMultiPartUploadForDatasetResponseDto(BaseModel):
    multipart_upload = MultiPartUploadDto


class ListDatasetsRequestDto(BaseModel):
    experiment_id: Optional[str] = None
    name: Optional[str] = None
    max_results: Optional[int] = None
    offset: Optional[int] = None
    page_token: Optional[str] = None


class ListDatasetsResponseDto(BaseModel):
    datasets: Optional[List[DatasetDto]]
    next_page_token: Optional[str]
    total: Optional[int]


class CreateMultiPartUploadRequestDto(BaseModel):
    artifact_version_id: str
    path: str
    num_parts: int
