from typing import List, Optional

from mlflow.dto.runs_dto import RunInfoDto
from mlflow.pydantic_v1 import BaseModel


class ExperimentTagDto(BaseModel):
    key: Optional[str]
    value: Optional[str]


class ExperimentDto(BaseModel):
    experiment_id: Optional[str]
    name: Optional[str]
    artifact_location: Optional[str]
    lifecycle_stage: Optional[str]
    tags: Optional[list[ExperimentTagDto]]
    creator_user_id: Optional[str]
    num_runs: Optional[int]
    num_user_collaborators: Optional[int]
    description: Optional[str]
    privacy_type: Optional[str]
    created_at: Optional[int]
    tenant_name: Optional[str]
    total_models_count: Optional[int]
    total_artifacts_count: Optional[int]
    storage_integration_id: Optional[str] = None


class ColumnsDto(BaseModel):
    metric_names: List[str]
    param_names: List[str]
    tag_names: List[str]


class EmptyResponse(BaseModel):
    pass


class ExperimentResponseDto(BaseModel):
    experiment: ExperimentDto


class CreateExperimentRequestDto(BaseModel):
    name: str
    # ambigious case, throws error even if it is Optional
    # Adding default value to handle such cases
    tags: Optional[List[ExperimentTagDto]]
    description: Optional[str]
    privacy_type: Optional[str]
    storage_integration_fqn: Optional[str]


class CreateExperimentResponseDto(BaseModel):
    experiment_id: str


class ListExperimentsResponseDto(BaseModel):
    experiments: List[ExperimentDto]
    next_page_token: Optional[str]
    total: Optional[int]


class ListSeedExperimentsResponseDto(BaseModel):
    experiments: List[ExperimentDto]


class GetExperimentResponseDto(BaseModel):
    experiment: ExperimentDto
    runs: Optional[List[RunInfoDto]]


class ExperimentIdRequestDto(BaseModel):
    experiment_id: str


class ListColumsResponseDto(BaseModel):
    columns: ColumnsDto


class UpdateExperimentRequestDto(BaseModel):
    experiment_id: str
    new_name: Optional[str]
    description: Optional[str]


class BackfillDefaultStorageIntegrationIdRequestDto(BaseModel):
    storage_integration_id: str


class SetExperimentTagRequestDto(BaseModel):
    experiment_id: str
    key: str
    value: str


class SetExperimentPrivacyTypeRequestDto(BaseModel):
    experiment_id: str
    privacy_type: str
