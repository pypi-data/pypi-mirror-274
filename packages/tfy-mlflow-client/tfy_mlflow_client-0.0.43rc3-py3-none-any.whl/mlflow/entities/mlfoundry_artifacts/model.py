import collections
import datetime
import uuid
from typing import Any, Dict, List, Optional

from mlflow.dto.mlfoundry_artifacts_dto import (
    FeatureDto,
    ModelDto,
    ModelSchemaDto,
    ModelVersionDto,
)
from mlflow.entities.experiment import Experiment
from mlflow.entities.metric import Metric
from mlflow.entities.mlfoundry_artifacts import utils
from mlflow.entities.mlfoundry_artifacts.artifact import (
    _ARTIFACT_VERSION_FQN_FORMAT,
    BaseArtifactMixin,
    BaseArtifactVersionMixin,
)
from mlflow.entities.mlfoundry_artifacts.custom_metric import CustomMetric
from mlflow.entities.mlfoundry_artifacts.enums import (
    ArtifactType,
    ArtifactVersionStatus,
    FeatureValueType,
    PredictionType,
)
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INVALID_PARAMETER_VALUE
from mlflow.pydantic_v1 import BaseModel, Field, constr, root_validator
from mlflow.utils.proto_json_utils import get_field_if_set

_MODEL_VERSION_USAGE_CODE_SNIPPET = """from truefoundry.ml import get_client
client = get_client()

# Get the model version directly
model_version = client.get_model_version_by_fqn("{fqn}")

# Download it to disk
# `download_info.model_dir` points to a directory which has contents of the model
download_info = model_version.download(path="your/download/location")
"""


class Model(BaseArtifactMixin):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        smart_union = True
        arbitrary_types_allowed = True

    id: uuid.UUID
    experiment_id: int
    experiment: Optional[Experiment] = None
    type: ArtifactType
    name: constr(regex=r"^[A-Za-z0-9_\-]+$", max_length=256)
    fqn: str
    description: Optional[constr(max_length=1024)] = None
    artifact_storage_root: str
    created_by: constr(max_length=256)
    latest_version: Optional["ModelVersion"] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    monitoring_enabled: bool = False

    def to_dto(self) -> ModelDto:
        return ModelDto(
            id=str(self.id),
            experiment_id=str(self.experiment_id),
            experiment=(self.experiment.to_dto() if self.experiment.name else None),
            type=self.type,
            name=self.name,
            fqn=self.fqn,
            artifact_storage_root=self.artifact_storage_root,
            description=self.description or "",
            created_by=self.created_by,
            created_at=self.created_at.astimezone(tz=datetime.timezone.utc).isoformat(),
            updated_at=self.updated_at.astimezone(tz=datetime.timezone.utc).isoformat(),
            monitoring_enabled=self.monitoring_enabled,
            latest_version=(
                self.latest_version.to_dto() if self.latest_version is not None else None
            ),
        )

    @classmethod
    def from_dto(cls, dto):
        latest_version = dto.latest_version
        if latest_version:
            latest_version = ModelVersion.from_dto(latest_version)
        experiment = dto.experiment
        if experiment:
            experiment = Experiment.from_dto(experiment)
        return cls(
            id=dto.id,
            experiment_id=dto.experiment_id,
            experiment=experiment,
            type=dto.type,
            name=dto.name,
            fqn=dto.fqn,
            artifact_storage_root=dto.artifact_storage_root,
            description=dto.description,
            created_by=dto.created_by,
            latest_version=latest_version,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            monitoring_enabled=dto.monitoring_enabled,
        )


class Feature(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        smart_union = True

    name: str
    type: FeatureValueType

    def to_dto(self) -> FeatureDto:
        return FeatureDto(name=self.name, type=FeatureValueType(self.type))


class ModelSchema(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = False
        smart_union = True

    features: List[Feature]
    prediction: PredictionType

    @property
    def actual(self):
        return self.prediction

    @staticmethod
    def _check_features_have_unique_names(features):
        name_counts = collections.Counter([f.name for f in features])
        duplicates = [name for name, count in name_counts.items() if count > 1]
        if duplicates:
            raise MlflowException(
                f"Found duplicates in given list of features. Names {duplicates} appear more than once. "
                f"All feature names must be unique",
                error_code=INVALID_PARAMETER_VALUE,
            )

    @root_validator(skip_on_failure=True)
    def validate_model_schema(cls, values):
        features = values["features"]
        cls._check_features_have_unique_names(features)
        return values

    def add_features(self, features: List[Feature]):
        self._check_features_have_unique_names(features)
        existing_features_dict = {f.name: f.dict() for f in self.features}
        for f in features:
            key = f.name
            value = f.dict()
            if key in existing_features_dict:
                if existing_features_dict[key] != value:
                    raise MlflowException(
                        f"Given feature {f.dict()!r} cannot be set, as a feature with name {f.name!r} "
                        f"is already set with config {existing_features_dict[key]!r}",
                        error_code=INVALID_PARAMETER_VALUE,
                    )
                continue
            self.features.append(f)

    @staticmethod
    def _check_prediction_type_is_consistent(
        existing_model_schemas: List["ModelSchemaWithMetadata"], new_model_schema: "ModelSchema"
    ):
        errors = []
        existing_model_schemas.sort(key=lambda mswm: mswm.version)
        prediction = None
        for schema in existing_model_schemas:
            if prediction is None:
                prediction = schema.prediction
                continue
            if schema.prediction != prediction:
                # ideally this should never happen as it would mean db is inconsistent
                errors.append(
                    f"`prediction` type in model schema for version {schema.version} is inconsistent with other "
                    f"model versions in this collection - expected {prediction!r} but it has {schema.prediction!r}"
                )
        if prediction is not None and new_model_schema.prediction != prediction:
            errors.append(
                f"`prediction` type in model schema is inconsistent with other model versions in this collection "
                f"- expected {prediction!r} but it has {new_model_schema.prediction!r}"
            )
        return errors

    @staticmethod
    def _check_features_are_consistent(
        existing_model_schemas: List["ModelSchemaWithMetadata"], new_model_schema: "ModelSchema"
    ):
        errors = []
        feature_dict = {}
        for schema in existing_model_schemas:
            for feature in schema.features:
                if feature.name in feature_dict:
                    if feature.type != feature_dict[feature.name]:
                        # ideally this should never happen as it would mean db is inconsistent
                        errors.append(
                            f"`feature` with name {feature.name!r} in model schema for version {schema.version} "
                            f"has inconsistent type with other model versions in this collection - "
                            f"expected type {feature_dict[feature.name]!r} but got {feature.type!r}"
                        )
                    continue
                feature_dict[feature.name] = feature.type
        for feature in new_model_schema.features:
            if feature.name in feature_dict:
                if feature.type != feature_dict[feature.name]:
                    errors.append(
                        f"`feature` with name {feature.name!r} in model schema "
                        f"has inconsistent type with other model versions in this collection - "
                        f"expected type {feature_dict[feature.name]!r} but got {feature.type!r}"
                    )
                continue
            feature_dict[feature.name] = feature.type
        return errors

    @staticmethod
    def check_mergeability(
        existing_model_schemas: List["ModelSchemaWithMetadata"], new_model_schema: "ModelSchema"
    ):
        errors = ModelSchema._check_prediction_type_is_consistent(
            existing_model_schemas=existing_model_schemas, new_model_schema=new_model_schema
        )
        feature_errors = ModelSchema._check_features_are_consistent(
            existing_model_schemas=existing_model_schemas, new_model_schema=new_model_schema
        )
        errors.extend(feature_errors)
        if errors:
            raise MlflowException(
                "Schema merging and validation failed, encountered following errors: \n"
                + "\n-> ".join(errors),
                error_code=INVALID_PARAMETER_VALUE,
            )

    @staticmethod
    def check_new_features_has_all_old_features(
        old_features: List[Feature], new_features: List[Feature]
    ):
        new_features = {nf.name for nf in new_features}
        missing_features = [of.name for of in old_features if of.name not in new_features]
        if missing_features:
            raise MlflowException(
                f"Features {missing_features!r} are missing from list of features in new schema. All existing "
                f"features must be provided in addition to any new features"
            )

    def to_dto(self):
        return ModelSchemaDto(
            features=[feature.to_dto() for feature in self.features], prediction=self.prediction
        )


# only meant for server side use, do not export this
class ModelSchemaWithMetadata(ModelSchema):
    id: uuid.UUID
    version: int


class ModelVersion(BaseArtifactVersionMixin):
    class Config:
        orm_mode = True
        validate_assignment = True
        use_enum_values = True
        allow_mutation = True
        smart_union = True
        arbitrary_types_allowed = True  # added because `Metric` is not a pydantic model

    id: uuid.UUID
    model_id: uuid.UUID
    model_name: str  # from relation
    model_fqn: str  # from relation
    experiment_id: int  # from relation
    version: int
    artifact_storage_root: str
    artifact_metadata: Dict[str, Any] = Field(default_factory=dict)
    data_path: Optional[str] = None
    description: Optional[constr(max_length=1024)] = None
    status: ArtifactVersionStatus
    step: Optional[int] = None
    metrics: List[Metric] = Field(default_factory=list)
    model_schema: Optional[ModelSchema] = None
    custom_metrics: Optional[List[CustomMetric]] = Field(default_factory=list)
    monitoring_enabled: bool = False
    run_id: Optional[str] = None  # from events
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_framework: Optional[str] = None
    artifact_size: Optional[int] = None

    @property
    def fqn(self) -> str:
        return _ARTIFACT_VERSION_FQN_FORMAT.format(
            artifact_fqn=self.model_fqn, version=self.version
        )

    @property
    def _usage_code_snippet(self) -> str:
        return _MODEL_VERSION_USAGE_CODE_SNIPPET.format(fqn=self.fqn)

    @staticmethod
    def _check_custom_metrics_have_unique_names(custom_metrics):
        name_counts = collections.Counter([cm.name for cm in custom_metrics])
        duplicates = [name for name, count in name_counts.items() if count > 1]
        if duplicates:
            raise MlflowException(
                f"Found duplicates in given list of custom metrics. Names {duplicates} appear more than once. "
                f"All custom metric names must be unique",
                error_code=INVALID_PARAMETER_VALUE,
            )

    @root_validator(skip_on_failure=True)
    def validate_custom_metrics(cls, values):
        model_schema = values["model_schema"]
        custom_metrics = values["custom_metrics"] or []
        if custom_metrics and not model_schema:
            raise MlflowException(
                "custom_metrics cannot be set without setting the schema first",
                error_code=INVALID_PARAMETER_VALUE,
            )
        cls._check_custom_metrics_have_unique_names(custom_metrics)
        return values

    @classmethod
    def from_dto(cls, dto):
        artifact_metadata = dto.artifact_metadata
        if artifact_metadata:
            artifact_metadata = dict(artifact_metadata)
        model_schema = dto.model_schema
        custom_metrics = dto.custom_metrics

        metrics = []
        if dto.metrics is not None:
            metrics = [Metric.from_dto(metric) for metric in dto.metrics]
        return cls(
            id=dto.id,
            metrics=metrics,
            model_id=dto.model_id,
            model_name=dto.model_name,
            model_fqn=dto.model_fqn,
            experiment_id=dto.experiment_id,
            version=dto.version,
            artifact_storage_root=dto.artifact_storage_root,
            artifact_metadata=artifact_metadata,
            data_path=dto.data_path,
            description=dto.description,
            status=dto.status,
            step=dto.step,
            model_schema=model_schema,
            custom_metrics=custom_metrics,
            monitoring_enabled=dto.monitoring_enabled,
            run_id=dto.run_id,
            created_by=dto.created_by,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            model_framework=dto.model_framework,
            artifact_size=dto.artifact_size,
        )

    def to_dto(self) -> ModelVersionDto:
        return ModelVersionDto(
            id=str(self.id),
            model_id=str(self.model_id),
            version=str(self.version),
            fqn=self.fqn,
            artifact_storage_root=self.artifact_storage_root,
            artifact_metadata=self.artifact_metadata if self.artifact_metadata is not None else {},
            description=self.description,
            status=self.status,
            step=self.step,
            created_by=self.created_by,
            model_schema=(self.model_schema.to_dto() if self.model_schema else None),
            custom_metrics=self.custom_metrics,
            created_at=self.created_at.isoformat() if self.created_at else None,
            updated_at=self.updated_at.isoformat() if self.updated_at else None,
            model_fqn=self.model_fqn,
            data_path=self.data_path,
            monitoring_enabled=self.monitoring_enabled,
            experiment_id=self.experiment_id,
            run_id=self.run_id,
            metrics=([metric.to_dto() for metric in self.metrics] if self.metrics else None),
            model_name=self.model_name,
            model_framework=self.model_framework,
            artifact_size=self.artifact_size,
            usage_code_snippet=self._usage_code_snippet,
        )

    def add_custom_metrics(self, custom_metrics: List[CustomMetric]):
        if custom_metrics and not self.model_schema:
            raise MlflowException(
                "custom_metrics cannot be set without setting the schema first",
                error_code=INVALID_PARAMETER_VALUE,
            )
        self._check_custom_metrics_have_unique_names(custom_metrics)
        existing_cm_dict = {cm.name: cm.dict() for cm in self.custom_metrics}
        for cm in custom_metrics:
            key = cm.name
            value = cm.dict()
            if key in existing_cm_dict:
                if existing_cm_dict[key] != value:
                    raise MlflowException(
                        f"Given custom metric {cm.dict()!r} cannot be set, as a custom metric with name {cm.name!r} "
                        f"is already set with config {cm.dict()!r}",
                        error_code=INVALID_PARAMETER_VALUE,
                    )
                continue
            self.custom_metrics.append(cm)


Model.update_forward_refs()
