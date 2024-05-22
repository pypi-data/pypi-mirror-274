from mlflow.dto.experiments_dto import ExperimentDto, ExperimentTagDto
from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.entities.auth_enums import PrivacyType
from mlflow.entities.experiment_tag import ExperimentTag
from mlflow.exceptions import MlflowException


class Experiment(_MLflowObject):
    """
    Experiment object.
    """

    DEFAULT_EXPERIMENT_NAME = "Default"

    def __init__(
        self,
        experiment_id,
        name,
        artifact_location,
        lifecycle_stage,
        tags=None,
        creator_user_id=None,
        num_runs=None,
        num_user_collaborators=None,
        description=None,
        privacy_type=PrivacyType.PRIVATE,
        created_at=None,
        tenant_name=None,
        total_models_count=None,
        total_artifacts_count=None,
        storage_integration_id=None,
    ):
        super().__init__()
        self._experiment_id = experiment_id
        self._name = name
        self._artifact_location = artifact_location
        self._lifecycle_stage = lifecycle_stage
        self._tags = {tag.key: tag.value for tag in (tags or [])}
        self._creator_user_id = creator_user_id
        self._num_runs = num_runs
        self._num_user_collaborators = num_user_collaborators
        self._description = description
        self._privacy_type = PrivacyType(privacy_type)
        self._created_at = created_at
        self._tenant_name = tenant_name
        self._storage_integration_id = storage_integration_id
        self._total_models_count = total_models_count
        self._total_artifacts_count = total_artifacts_count

    @property
    def experiment_id(self):
        """String ID of the experiment."""
        return self._experiment_id

    @property
    def name(self):
        """String name of the experiment."""
        return self._name

    def _set_name(self, new_name):
        self._name = new_name

    @property
    def artifact_location(self) -> str:
        """String corresponding to the root artifact URI for the experiment."""
        return self._artifact_location

    @property
    def lifecycle_stage(self):
        """Lifecycle stage of the experiment. Can either be 'active' or 'deleted'."""
        return self._lifecycle_stage

    @property
    def creator_user_id(self):
        """user_id of the creator of the experiment"""
        return self._creator_user_id

    @property
    def num_runs(self):
        return self._num_runs

    @property
    def num_user_collaborators(self):
        return self._num_user_collaborators

    @property
    def tags(self):
        """Tags that have been set on the experiment."""
        return self._tags

    def _add_tag(self, tag):
        self._tags[tag.key] = tag.value

    @property
    def description(self):
        return self._description

    @property
    def privacy_type(self):
        return self._privacy_type

    @property
    def created_at(self):
        return self._created_at

    @property
    def tenant_name(self):
        if not self._tenant_name:
            raise MlflowException("tenant_name is not set")
        return self._tenant_name

    @property
    def storage_integration_id(self):
        return self._storage_integration_id

    @property
    def total_models_count(self):
        return self._total_models_count

    @property
    def total_artifacts_count(self):
        return self._total_artifacts_count

    def to_dto(self) -> ExperimentDto:
        return ExperimentDto(
            experiment_id=self.experiment_id,
            name=self.name,
            artifact_location=self.artifact_location,
            lifecycle_stage=self.lifecycle_stage,
            tags=[ExperimentTagDto(key=key, value=value) for key, value in self.tags.items()],
            creator_user_id=self.creator_user_id,
            num_runs=self.num_runs,
            num_user_collaborators=self.num_user_collaborators,
            description=self.description,
            privacy_type=self.privacy_type.value,
            created_at=self.created_at,
            tenant_name=self.tenant_name,
            total_models_count=self.total_models_count,
            total_artifacts_count=self.total_artifacts_count,
            storage_integration_id=self.storage_integration_id,
        )

    @classmethod
    def from_dto(cls, dto):
        experiment = cls(
            dto.experiment_id,
            dto.name,
            dto.artifact_location,
            dto.lifecycle_stage,
            creator_user_id=dto.creator_user_id,
            num_runs=dto.num_runs,
            num_user_collaborators=dto.num_user_collaborators,
            description=dto.description,
            privacy_type=dto.privacy_type,
            created_at=dto.created_at,
            tenant_name=dto.tenant_name,
            total_models_count=dto.total_models_count,
            total_artifacts_count=dto.total_artifacts_count,
            storage_integration_id=dto.storage_integration_id,
        )
        if dto.tags is not None:
            for dto_tag in dto.tags:
                experiment._add_tag(ExperimentTag.from_dto(dto_tag))
        return experiment
