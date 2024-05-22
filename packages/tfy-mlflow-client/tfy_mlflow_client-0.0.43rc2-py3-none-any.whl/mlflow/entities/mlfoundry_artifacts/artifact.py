import datetime
import posixpath
import uuid
from typing import Any, Dict, List, Optional, Tuple

from mlflow.dto.mlfoundry_artifacts_dto import ArtifactDto, ArtifactVersionDto
from mlflow.entities.experiment import Experiment
from mlflow.entities.mlfoundry_artifacts import utils
from mlflow.entities.mlfoundry_artifacts.enums import (
    ArtifactType,
    ArtifactVersionStatus,
)
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from mlflow.pydantic_v1 import BaseModel, Field, constr
from mlflow.utils.uri import append_to_uri_path

_ARTIFACT_FQN_FORMAT = "{artifact_type}:{tenant_name}/{experiment_name}/{artifact_name}"
_ARTIFACT_VERSION_FQN_FORMAT = "{artifact_fqn}:{version}"

_ARTIFACT_VERSION_USAGE_CODE_SNIPPET = """from truefoundry.ml import get_client
client = get_client()

# Get the artifact version directly
artifact_version = client.get_artifact_version_by_fqn("{fqn}")

# download it to disk
# `download_path` points to a directory that has all contents of the artifact
download_path = artifact_version.download(path="your/download/location")"""


class BaseArtifactMixin(BaseModel):
    @staticmethod
    def generate_fqn(
        experiment: Experiment, artifact_type: ArtifactType, artifact_name: str
    ) -> str:
        if not experiment.tenant_name:
            raise ValueError(f"Attributes `tenant_name` on `experiment` cannot be None")
        return _ARTIFACT_FQN_FORMAT.format(
            artifact_type=artifact_type.value,
            tenant_name=experiment.tenant_name,
            experiment_name=experiment.name,
            artifact_name=artifact_name,
        )

    @staticmethod
    def generate_storage_root(
        experiment: Experiment, artifact_type: ArtifactType, artifact_name: str
    ) -> str:
        # noinspection PyTypeChecker
        return append_to_uri_path(
            experiment.artifact_location,
            "artifacts",
            artifact_type.value,
            artifact_name,
            posixpath.sep,
        )


class Artifact(BaseArtifactMixin):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        smart_union = True

    id: uuid.UUID
    experiment_id: int
    type: ArtifactType
    name: constr(regex=r"^[A-Za-z0-9_\-]+$", max_length=256)
    fqn: str
    description: Optional[constr(max_length=1024)] = None
    artifact_storage_root: str
    created_by: constr(max_length=256)
    latest_version: Optional["ArtifactVersion"] = None
    run_steps: List[int] = Field(default_factory=list)

    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dto(self) -> ArtifactDto:
        return ArtifactDto(
            id=str(self.id),
            experiment_id=self.experiment_id,
            type=self.type,
            name=self.name,
            fqn=self.fqn,
            description=self.description,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
            artifact_storage_root=self.artifact_storage_root,
            latest_version=self.latest_version.to_dto() if self.latest_version else None,
            run_steps=self.run_steps,
        )

    @classmethod
    def from_dto(cls, dto):
        latest_version = dto.latest_version
        if latest_version:
            latest_version = ArtifactVersion.from_dto(latest_version)
        return cls(
            id=dto.id,
            experiment_id=dto.experiment_id,
            type=dto.type,
            name=dto.name,
            fqn=dto.fqn,
            artifact_storage_root=dto.artifact_storage_root,
            description=dto.description,
            created_by=dto.created_by,
            latest_version=latest_version,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            run_steps=dto.run_steps,
        )


class BaseArtifactVersionMixin(BaseModel):
    @property
    def fqn(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def get_artifact_fqn_and_version(fqn: str) -> Tuple[str, int]:
        try:
            artifact_fqn, version = fqn.rsplit(":", 1)
        except ValueError:
            raise MlflowException(
                f"Invalid value for fqn: {fqn!r}. Expected format "
                "{type}:{tenant}/{username}/{project}/{model_name}:{version}",
                error_code=INVALID_PARAMETER_VALUE,
            )

        if (
            version == "latest"
        ):  # Temporarily added as convenience, ideally should be managed using tags
            version = -1
        else:
            try:
                version = int(version)
            except:
                raise MlflowException(
                    f"The given `fqn` {fqn!r} is invalid. The expected format for fqn is "
                    "{type}:{tenant}/{username}/{project}/{model_name}:{version} where the version must be an integer",
                    error_code=INVALID_PARAMETER_VALUE,
                )
        return artifact_fqn, version


class ArtifactVersion(BaseArtifactVersionMixin):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = True
        smart_union = True

    id: uuid.UUID
    artifact_id: uuid.UUID
    artifact_name: str  # from relation
    artifact_fqn: str  # from relation
    experiment_id: int  # from relation
    version: int
    artifact_storage_root: str
    artifact_metadata: Dict[str, Any] = Field(default_factory=dict)
    data_path: Optional[str] = None
    description: Optional[constr(max_length=1024)] = None
    status: ArtifactVersionStatus
    step: Optional[int] = None
    run_id: Optional[str] = None  # also stored in events
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    internal_metadata: Optional[Dict[str, Any]] = None
    artifact_size: Optional[int] = None

    @property
    def fqn(self) -> str:
        return _ARTIFACT_VERSION_FQN_FORMAT.format(
            artifact_fqn=self.artifact_fqn, version=self.version
        )

    @property
    def _usage_code_snippet(self) -> str:
        return _ARTIFACT_VERSION_USAGE_CODE_SNIPPET.format(fqn=self.fqn)

    def to_dto(self) -> ArtifactVersionDto:
        return ArtifactVersionDto(
            id=str(self.id),
            artifact_id=str(self.artifact_id),
            version=self.version,
            fqn=self.fqn,
            artifact_storage_root=self.artifact_storage_root,
            artifact_metadata=self.artifact_metadata,
            description=self.description,
            status=self.status,
            step=self.step,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
            artifact_fqn=self.artifact_fqn,
            data_path=self.data_path,
            usage_code_snippet=self._usage_code_snippet,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            artifact_name=self.artifact_name,
            internal_metadata=self.internal_metadata,
            artifact_size=self.artifact_size,
        )

    @classmethod
    def from_dto(cls, dto):
        artifact_metadata = dto.artifact_metadata
        internal_metadata = dto.internal_metadata
        return cls(
            id=dto.id,
            artifact_id=dto.artifact_id,
            artifact_name=dto.artifact_name,
            artifact_fqn=dto.artifact_fqn,
            experiment_id=dto.experiment_id,
            version=dto.version,
            artifact_storage_root=dto.artifact_storage_root,
            artifact_metadata=artifact_metadata,
            data_path=dto.data_path,
            description=dto.description,
            status=dto.status,
            step=dto.step,
            run_id=dto.run_id,
            created_by=dto.created_by,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            internal_metadata=internal_metadata,
            artifact_size=dto.artifact_size,
        )


Artifact.update_forward_refs()
