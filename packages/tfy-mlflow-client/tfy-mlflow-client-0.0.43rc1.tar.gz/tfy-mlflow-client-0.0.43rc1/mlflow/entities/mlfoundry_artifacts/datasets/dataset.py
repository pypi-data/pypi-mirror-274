import datetime
import posixpath
import uuid
from typing import Any, Dict, Optional

from mlflow.dto.mlfoundry_artifacts_dto import DatasetDto
from mlflow.entities.experiment import Experiment
from mlflow.entities.mlfoundry_artifacts import utils
from mlflow.pydantic_v1 import BaseModel, constr
from mlflow.utils.proto_json_utils import get_field_if_set
from mlflow.utils.uri import append_to_uri_path

_DATASET_FQN_FORMAT = "data-dir:{tenant_name}/{experiment_name}/{artifact_name}"

_DATASET_USAGE_CODE_SNIPPET = """from truefoundry.ml import get_client
client = get_client()

# Get the dataset directly
dataset = client.get_data_directory_by_fqn(fqn="{fqn}")

# download it to disk
dataset.download(path="your/download/location")"""


class Dataset(BaseModel):
    @staticmethod
    def generate_fqn(experiment: Experiment, name: str) -> str:
        if not experiment.tenant_name:
            raise ValueError(f"Attributes `tenant_name` on `experiment` cannot be None")
        return _DATASET_FQN_FORMAT.format(
            tenant_name=experiment.tenant_name,
            experiment_name=experiment.name,
            artifact_name=name,
        )

    @staticmethod
    def generate_storage_root(experiment: Experiment, name: str) -> str:
        # noinspection PyTypeChecker
        return append_to_uri_path(
            experiment.artifact_location, "artifacts", "datasets", name, posixpath.sep
        )

    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        smart_union = True
        arbitrary_types_allowed = True  # added because experiment is not a pydantic model

    id: uuid.UUID
    experiment_id: int
    experiment: Optional[Experiment] = None
    name: constr(regex=r"^[A-Za-z0-9_\-]+$", max_length=256)
    fqn: str
    description: Optional[constr(max_length=1024)] = None
    storage_root: str
    dataset_metadata: Optional[Dict[str, Any]] = None
    created_by: constr(max_length=256)
    created_at: datetime.datetime
    updated_at: datetime.datetime

    @property
    def _usage_code_snippet(self) -> str:
        return _DATASET_USAGE_CODE_SNIPPET.format(fqn=self.fqn)

    def to_dto(self) -> DatasetDto:
        return DatasetDto(
            id=str(self.id),
            experiment_id=str(self.experiment_id),
            experiment=self.experiment.to_dto() if self.experiment else None,
            name=self.name,
            fqn=self.fqn,
            description=self.description,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
            storage_root=self.storage_root,
            dataset_metadata=self.dataset_metadata,
            usage_code_snippet=self._usage_code_snippet,
        )

    @classmethod
    def from_dto(cls, dto):
        dataset_metadata = dto.dataset_metadata
        if dataset_metadata:
            dataset_metadata = dict(dataset_metadata)
        experiment = dto.experiment
        if experiment:
            experiment = Experiment.from_dto(experiment)
        return cls(
            id=dto.id,
            experiment_id=dto.experiment_id,
            experiment=experiment,
            name=dto.name,
            fqn=dto.fqn,
            storage_root=dto.storage_root,
            description=dto.description,
            created_by=dto.created_by,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            dataset_metadata=dataset_metadata,
            usage_code_snippet=dto.usage_code_snippet,
        )
