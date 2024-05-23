import json
import typing
import uuid

from mlflow.config import config
from mlflow.dto.experiments_dto import EmptyResponse
from mlflow.dto.runs_dto import RunLogInputDto
from mlflow.entities import (
    SENTINEL,
    Artifact,
    ArtifactType,
    ArtifactVersion,
    ArtifactVersionStatus,
    CustomMetric,
    Dataset,
    Experiment,
    Feature,
    FileInfo,
    Metric,
    Model,
    ModelSchema,
    ModelVersion,
    MultiPartUpload,
    Run,
    RunInfo,
    RunLog,
    SignedURL,
    ViewType,
)
from mlflow.entities.mlfoundry_artifacts.utils import dict_to_proto
from mlflow.entities.run_status import RunStatus
from mlflow.exceptions import MlflowException
from mlflow.protos import databricks_pb2
from mlflow.store.entities.paged_list import PagedList
from mlflow.store.tracking.abstract_store import AbstractStore
from mlflow.utils.rest_utils import call_endpoint


class RestStore(AbstractStore):
    """
    Client for a remote tracking server accessed via REST API calls

    :param get_host_creds: Method to be invoked prior to every REST request to get the
      :py:class:`mlflow.rest_utils.MlflowHostCreds` for the request. Note that this
      is a function so that we can obtain fresh credentials in the case of expiry.
    """

    def __init__(self, get_host_creds):
        super().__init__()
        self.get_host_creds = get_host_creds

    def _call_endpoint(self, api, json_body):
        endpoint, method = api.path, api.method
        if json_body:
            json_body = json.loads(json_body)
        response_dto_cls = api.response_dto
        if response_dto_cls is None:
            response_dto_cls = EmptyResponse
        return call_endpoint(self.get_host_creds(), endpoint, method, json_body, response_dto_cls)

    def list_experiments(
        self,
        ids=None,
        view_type=ViewType.ACTIVE_ONLY,
        max_results=None,
        page_token=None,
    ):
        """
        :param view_type: Qualify requested type of experiments.
        :param max_results: If passed, specifies the maximum number of experiments desired. If not
                            passed, the server will pick a maximum number of results to return.
        :param page_token: Token specifying the next page of results. It should be obtained from
                            a ``list_experiments`` call.
        :param ids: list of experiment ids - which you want to return
                    [Currently not implemented for rest store]
        :return: A :py:class:`PagedList <mlflow.store.entities.PagedList>` of
                 :py:class:`Experiment <mlflow.entities.Experiment>` objects. The pagination token
                 for the next page can be obtained via the ``token`` attribute of the object.
        """
        req_body = json.dumps(
            {
                "view_type": view_type,
                "max_results": max_results,
                "page_token": page_token,
            }
        )

        response_dto = self._call_endpoint(config.ListExperiment, req_body)
        experiments = [Experiment.from_dto(x) for x in response_dto.experiments]
        next_page_token = response_dto.next_page_token
        return PagedList(experiments, next_page_token)

    def create_experiment(self, name, tags=None, description=None, storage_integration_fqn=None):
        """
        Create a new experiment.
        If an experiment with the given name already exists, throws exception.

        :param name: Desired name for an experiment
        :param tags: Experiment tags to set upon experiment creation
        :param description: Experiment description to set upon experiment creation
        :param storage_integration_fqn: Storage integration fqn to set upon experiment creation. can be none (default will be chosen)

        :return: experiment_id (string) for the newly created experiment if successful, else None

        """
        tags_dtos = [tag.to_dto() for tag in tags] if tags else []
        req_body = config.CreateExperiment.request_dto(
            tags=tags_dtos,
            name=name,
            description=description,
            storage_integration_fqn=storage_integration_fqn,
        ).json()

        response_dto = self._call_endpoint(config.CreateExperiment, req_body)
        return response_dto.experiment_id

    def get_experiment(self, experiment_id):
        """
        Fetch the experiment from the backend store.

        :param experiment_id: String id for the experiment

        :return: A single :py:class:`mlflow.entities.Experiment` object if it exists,
        otherwise raises an Exception.
        """
        req_body = json.dumps({"experiment_id": experiment_id})
        response_dto = self._call_endpoint(config.GetExperiment, req_body)
        return Experiment.from_dto(response_dto.experiment)

    # TODO: Convert to DTO
    def delete_experiment(self, experiment_id):
        req_body = config.DeleteExperiment.request_dto(experiment_id=str(experiment_id)).json()
        self._call_endpoint(config.DeleteExperiment, req_body)

    def restore_experiment(self, experiment_id):
        req_body = config.RestoreExperiment.request_dto(experiment_id=experiment_id).json()

        self._call_endpoint(config.RestoreExperiment, req_body)

    def rename_experiment(self, experiment_id, new_name):
        req_body = config.UpdateExperiment.request_dto(
            experiment_id=experiment_id, new_name=new_name
        ).json()

        self._call_endpoint(config.UpdateExperiment, req_body)

    def update_experiment(self, experiment_id, description):
        req_body = config.UpdateExperiment.request_dto(
            experiment_id=experiment_id, description=description
        ).json()

        self._call_endpoint(config.UpdateExperiment, req_body)

    def get_run(self, run_id):
        """
        Fetch the run from backend store

        :param run_id: Unique identifier for the run

        :return: A single Run object if it exists, otherwise raises an Exception
        """
        req_body = json.dumps({"run_id": run_id})
        response_dto = self._call_endpoint(config.GetRun, req_body)
        return Run.from_dto(response_dto.run)

    def update_run_info(self, run_id, run_status=None, end_time=None, description=SENTINEL):
        """Updates the metadata of the specified run."""
        updated_run_info = {}
        if run_status is not None:
            # Convert to string here, always send string to endpoint
            # By default it comes as int
            updated_run_info["status"] = RunStatus.to_string(run_status)
        if end_time is not None:
            updated_run_info["end_time"] = end_time
        if description is not SENTINEL:
            updated_run_info["description"] = description or ""
        updated_run_info = {
            key: value for key, value in updated_run_info.items() if value is not SENTINEL
        }
        req_body = config.UpdateRun.request_dto(run_id=run_id, **updated_run_info).json()
        response_dto = self._call_endpoint(config.UpdateRun, req_body)
        return RunInfo.from_dto(response_dto.run_info)

    def create_run(self, experiment_id, user_id, start_time, tags, name, description):
        """
        Create a run under the specified experiment ID, setting the run's status to "RUNNING"
        and the start time to the current time.

        :param experiment_id: ID of the experiment for this run
        :param user_id: ID of the user launching this run
        :param start_time: timestamp of the initialization of the run
        :param tags: tags to apply to this run at initialization

        :return: The created Run object
        """
        tag_dtos = [tag.to_dto() for tag in tags]
        req_body = config.CreateRun.request_dto(
            experiment_id=experiment_id,
            user_id=user_id,
            start_time=start_time,
            tags=tag_dtos,
            description=description,
            name=name,
        ).json()
        response_dto = self._call_endpoint(config.CreateRun, req_body)
        run = Run.from_dto(response_dto.run)
        return run

    def log_metric(self, run_id, metric):
        """
        Log a metric for the specified run

        :param run_id: String id for the run
        :param metric: Metric instance to log
        """
        req_body = config.LogMetric.request_dto(
            run_id=run_id, key=metric.key, value=metric.value
        ).json()
        self._call_endpoint(config.LogMetric, req_body)

    def log_param(self, run_id, param):
        """
        Log a param for the specified run

        :param run_id: String id for the run
        :param param: Param instance to log
        """
        req_body = config.LogParameter.request_dto(
            run_uuid=run_id, run_id=run_id, key=param.key, value=param.value
        ).json()

        self._call_endpoint(config.LogParam, req_body)

    def set_experiment_tag(self, experiment_id, tag):
        """
        Set a tag for the specified experiment

        :param experiment_id: String ID of the experiment
        :param tag: ExperimentRunTag instance to log
        """
        req_body = config.SetExperimentTag.request_dto(
            experiment_id=experiment_id, key=tag.key, value=tag.value
        ).json()
        self._call_endpoint(config.SetExperimentTag, req_body)

    def set_tag(self, run_id, tag):
        """
        Set a tag for the specified run

        :param run_id: String ID of the run
        :param tag: RunTag instance to log
        """
        req_body = config.SetTag.request_dto(
            run_uuid=run_id, run_id=run_id, key=tag.key, value=tag.value
        ).json()
        self._call_endpoint(config.SetTag, req_body)

    def delete_tag(self, run_id, key):
        """
        Delete a tag from a run. This is irreversible.
        :param run_id: String ID of the run
        :param key: Name of the tag
        """
        req_body = config.DeleteTag.request_dto(run_id=run_id, key=key).json()
        self._call_endpoint(config.DeleteTag, req_body)

    def get_metric_history(self, run_id, metric_key):
        """
        Return all logged values for a given metric.

        :param run_id: Unique identifier for run
        :param metric_key: Metric name within the run

        :return: A list of :py:class:`mlflow.entities.Metric` entities if logged, else empty list
        """
        req_body = json.dumps({"run_uuid": run_id, "run_id": run_id, "metric_key": metric_key})
        response_dto = self._call_endpoint(config.GetMetricHistory, req_body)
        return [Metric.from_dto(metric) for metric in response_dto.metrics]

    def _search_runs(
        self, experiment_ids, filter_string, run_view_type, max_results, order_by, page_token
    ):
        experiment_ids = [str(experiment_id) for experiment_id in experiment_ids]
        sr = config.SearchRuns.request_dto(
            experiment_ids=experiment_ids,
            filter=filter_string,
            run_view_type=ViewType.to_string(run_view_type),
            max_results=max_results,
            order_by=order_by,
            page_token=page_token,
        )
        req_body = sr.json()
        response_dto = self._call_endpoint(config.SearchRuns, req_body)
        runs = [Run.from_dto(run_dto) for run_dto in response_dto.runs]
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        return runs, next_page_token

    def delete_run(self, run_id):
        req_body = config.DeleteRun.request_dto(run_id=run_id).json()
        self._call_endpoint(config.DeleteRun, req_body)

    def hard_delete_run(self, run_id):
        req_body = config.HardDeleteRun.request_dto(run_id=run_id).json()
        self._call_endpoint(config.HardDeleteRun, req_body)

    def restore_run(self, run_id):
        req_body = config.RestoreRun.request_dto(run_id=run_id).json()
        self._call_endpoint(config.RestoreRun, req_body)

    def get_experiment_by_name(
        self,
        experiment_name,
        tenant_name: typing.Optional[str] = None,
    ):
        try:
            req_body = json.dumps({"experiment_name": experiment_name})
            response_dto = self._call_endpoint(config.GetExperimentByName, req_body)
            return Experiment.from_dto(response_dto.experiment)
        except MlflowException as e:
            if e.error_code == databricks_pb2.ErrorCode.Name(
                databricks_pb2.RESOURCE_DOES_NOT_EXIST
            ):
                return None
            raise e

    def log_batch(self, run_id, metrics, params, tags):
        metric_dtos = []
        if metrics:
            metric_dtos = [metric.to_dto() for metric in metrics]
        param_dtos = []
        if params:
            param_dtos = [param.to_dto() for param in params]
        tag_dtos = []
        if tags:
            tag_dtos = [tag.to_dto() for tag in tags if tag is not None]
        req_body = config.LogRunBatch.request_dto(
            metrics=metric_dtos, params=param_dtos, tags=tag_dtos, run_id=run_id
        ).json()
        self._call_endpoint(config.LogRunBatch, req_body)

    def record_logged_model(self, run_id, mlflow_model):
        req_body = config.LogModel.request_dto(
            run_id=run_id, model_json=mlflow_model.to_json()
        ).json()
        self._call_endpoint(config.LogModel, req_body)

    def insert_run_logs(self, run_uuid: str, run_logs: typing.List[RunLog]):
        request_body_dto = config.RunLogs.request_dto(
            run_uuid=run_uuid,
            run_logs=[
                RunLogInputDto(
                    key=run_log.key,
                    step=run_log.step,
                    timestamp=run_log.timestamp,
                    log_type=run_log.log_type,
                    value=run_log.value,
                    artifact_path=run_log.artifact_path,
                )
                for run_log in run_logs
            ],
        )

        request_body = request_body_dto.json()
        self._call_endpoint(config.RunLogs, request_body)

    def get_latest_run_log(self, run_uuid: str, key: str, log_type: str) -> RunLog:
        request_body = json.dumps({"run_uuid": run_uuid, "key": key, "log_type": log_type})
        response_dto = self._call_endpoint(config.LatestRunLog, request_body)
        return RunLog.from_dto(response_dto.run_log)

    def list_run_logs(
        self,
        run_uuid: str,
        key: typing.Optional[str] = None,
        log_type: typing.Optional[str] = None,
        steps: typing.Optional[typing.List[int]] = None,
    ) -> typing.List[RunLog]:
        request_body = json.dumps(
            {
                "run_uuid": run_uuid,
                "key": key or "",
                "log_type": log_type or "",
                "steps": steps or [],
            }
        )
        response_dto = self._call_endpoint(config.ListRunLogs, request_body)
        return [RunLog.from_dto(run_log) for run_log in response_dto.run_logs]

    def get_run_by_fqn(self, fqn: str) -> Run:
        request_body = json.dumps({"run_fqn": fqn})
        response_dto = self._call_endpoint(config.GetRunByFqn, request_body)
        return Run.from_dto(response_dto.run)

    def get_run_by_name(
        self,
        run_name: str,
        experiment_id: typing.Optional[str] = None,
        experiment_name: typing.Optional[str] = None,
    ) -> Run:
        request_body = json.dumps(
            {
                "run_name": run_name,
                "experiment_id": experiment_id,
                "experiment_name": experiment_name,
            }
        )
        response_dto = self._call_endpoint(config.GetRunByName, request_body)
        return Run.from_dto(response_dto.run)

    # Mlfoundry Artifacts methods
    # TODO (chiragjn): consider moving these to another store/mlfoundry_artifacts/rest_store.py
    # TODO (chiragjn): implement list apis for artifacts and models
    # TODO (chiragjn): get_artifact* and get_model* methods break LSP, they return T instead of Optional[T]

    def create_artifact_version(
        self,
        experiment_id: typing.Union[int, str],
        artifact_type: ArtifactType,
        name: str,
    ) -> uuid.UUID:
        message = config.CreateArtifactVersions.request_dto(
            experiment_id=str(experiment_id), name=name, artifact_type=artifact_type
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateArtifactVersions, request_body)
        return uuid.UUID(response_dto.id)

    def get_artifact_by_id(self, artifact_id: uuid.UUID, **kwargs) -> Artifact:
        message = {"id": str(artifact_id)}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetArtifactById, request_body)
        return Artifact.from_dto(response_dto.artifact)

    def get_artifact_by_fqn(
        self,
        fqn: str,
    ) -> Artifact:
        request_body = json.dumps({"fqn": fqn})
        response_dto = self._call_endpoint(config.GetArtifactByFqn, request_body)
        return Artifact.from_dto(response_dto.artifact)

    def notify_failure_for_artifact_version(
        self,
        version_id: uuid.UUID,
    ):
        message = config.NotifyFailure.request_dto(id=str(version_id))
        request_body = message.json()
        self._call_endpoint(config.NotifyFailure, request_body)

    def list_files_for_artifact_version(
        self,
        version_id: uuid.UUID,
        path: typing.Optional[str] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
    ) -> PagedList[FileInfo]:
        message = config.ListFilesForArtifactVersion.request_dto(
            id=str(version_id),
            path=path,
            max_results=max_results,
            page_token=page_token,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListFilesForArtifactVersion, request_body)
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        return PagedList(
            [FileInfo.from_dto(f) for f in response_dto.files],
            token=next_page_token,
        )

    def get_signed_urls_for_artifact_version_read(
        self, version_id: uuid.UUID, paths: typing.List[str]
    ) -> typing.List[SignedURL]:
        message = config.GetSignedUrlsForRead.request_dto(id=str(version_id), paths=paths)
        request_body = message.json()
        response_dto = self._call_endpoint(config.GetSignedUrlsForRead, request_body)
        return [SignedURL.from_dto(s) for s in response_dto.signed_urls]

    def get_signed_urls_for_artifact_version_write(
        self, version_id: uuid.UUID, paths: typing.List[str]
    ) -> typing.List[SignedURL]:
        message = config.GetSignedUrlsForWrite.request_dto(id=str(version_id), paths=paths)
        request_body = message.json()
        response_dto = self._call_endpoint(config.GetSignedUrlsForWrite, request_body)
        return [SignedURL.from_dto(s) for s in response_dto.signed_urls]

    def finalize_artifact_version(
        self,
        version_id: uuid.UUID,
        run_uuid: str = None,
        description: typing.Optional[str] = None,
        # this is only `Optional` because argument default should be {}
        artifact_metadata: typing.Optional[typing.Dict[str, typing.Any]] = None,
        data_path: typing.Optional[str] = None,
        step: int = 0,
        artifact_size: typing.Optional[int] = None,
        # unused args
        created_by: typing.Optional[str] = None,
    ) -> ArtifactVersion:
        artifact_metadata = artifact_metadata or {}
        message = config.FinalizeArtifactVersion.request_dto(
            id=str(version_id),
            run_uuid=run_uuid,
            description=description,
            artifact_metadata=dict_to_proto(artifact_metadata),
            data_path=data_path,
            step=step,
            artifact_size=artifact_size,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.FinalizeArtifactVersion, request_body)
        return ArtifactVersion.from_dto(response_dto.artifact_version)

    def get_artifact_version_by_id(
        self,
        version_id: uuid.UUID,
        # unused kwargs
        status: typing.Optional[ArtifactVersionStatus] = None,
    ) -> ArtifactVersion:
        message = {"id": str(version_id)}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetArtifactVersionById, request_body)
        return ArtifactVersion.from_dto(response_dto.artifact_version)

    def get_artifact_version(
        self,
        experiment_id: int,
        artifact_name: str,
        version: typing.Optional[int] = None,
        artifact_type: typing.Optional[ArtifactType] = ArtifactType.ARTIFACT,
    ) -> ArtifactVersion:
        kwargs = dict(
            experiment_id=experiment_id, artifact_name=artifact_name, artifact_type=artifact_type
        )
        if isinstance(artifact_type, ArtifactType):
            kwargs["artifact_type"] = str(artifact_type.value)
        if version:  # if version is not passed, latest version will be fetched
            kwargs["version"] = version
        message = kwargs
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetArtifactVersionByName, request_body)
        return ArtifactVersion.from_dto(response_dto.artifact_version)

    def get_artifact_version_by_fqn(
        self,
        fqn: str,
        # unused kwargs
        status: typing.Optional[ArtifactVersionStatus] = None,
    ) -> ArtifactVersion:
        message = {"fqn": fqn}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetArtifactVersionByFqn, request_body)
        return ArtifactVersion.from_dto(response_dto.artifact_version)

    def update_artifact_version(
        self,
        version_id: uuid.UUID,
        description: typing.Optional[str] = SENTINEL,
        artifact_metadata: typing.Dict[str, typing.Any] = SENTINEL,
    ) -> ArtifactVersion:
        kwargs = dict(description=description)
        if artifact_metadata is not SENTINEL:
            kwargs["artifact_metadata"] = dict_to_proto(artifact_metadata)
        kwargs = {k: v for k, v in kwargs.items() if v is not SENTINEL}
        message = config.UpdateArtifactVersions.request_dto(id=str(version_id), **kwargs)
        request_body = message.json()
        response_dto = self._call_endpoint(config.UpdateArtifactVersions, request_body)
        return ArtifactVersion.from_dto(response_dto.artifact_version)

    def delete_artifact_version(self, version_id: uuid.UUID):
        message = config.DeleteArtifactVersions.request_dto(id=str(version_id))
        request_body = message.json()
        self._call_endpoint(config.DeleteArtifactVersions, request_body)

    def get_model_by_id(
        self,
        model_id: uuid.UUID,
    ) -> Model:
        message = {"id": str(model_id)}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetModel, request_body)
        return Model.from_dto(response_dto.model)

    def get_model_by_fqn(
        self,
        fqn: str,
    ) -> Model:
        message = {"fqn": fqn}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetModelUsingFqn, request_body)
        return Model.from_dto(response_dto.model)

    def get_model_by_name(
        self,
        experiment_id: int,
        name: str,
    ) -> Model:
        message = {"experiment_id": experiment_id, "name": name}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetModelUsingName, request_body)
        return Model.from_dto(response_dto.model)

    def create_model_version(
        self,
        artifact_version_id: uuid.UUID,
        description: typing.Optional[str] = SENTINEL,
        artifact_metadata: typing.Dict[str, typing.Any] = SENTINEL,
        internal_metadata: typing.Dict[str, typing.Any] = SENTINEL,
        data_path: typing.Optional[str] = SENTINEL,
        step: typing.Optional[int] = SENTINEL,
    ) -> ModelVersion:
        kwargs = dict(
            description=description,
            data_path=data_path,
            internal_metadata=internal_metadata,
            step=step,
        )
        if artifact_metadata is not SENTINEL:
            kwargs["artifact_metadata"] = dict_to_proto(artifact_metadata)
        if internal_metadata is not SENTINEL:
            kwargs["internal_metadata"] = dict_to_proto(internal_metadata)
        kwargs = {k: v for k, v in kwargs.items() if v is not SENTINEL}
        message = config.CreateModelVersion.request_dto(
            artifact_version_id=str(artifact_version_id), **kwargs
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateModelVersion, request_body)
        return ModelVersion.from_dto(response_dto.model_version)

    def get_model_version_by_id(
        self,
        version_id: uuid.UUID,
        # unused kwargs
        status: typing.Optional[ArtifactVersionStatus] = None,
    ) -> ModelVersion:
        message = {"id": str(version_id)}
        request_body = json.loads(message)
        response_dto = self._call_endpoint(config.GetModelVersion, request_body)
        return ModelVersion.from_dto(response_dto.model_version)

    def get_model_version(
        self,
        experiment_id: int,
        model_name: str,
        version: typing.Optional[int] = None,
    ) -> ModelVersion:
        kwargs = dict(experiment_id=experiment_id, model_name=model_name)
        if version:  # if version is not passed, latest version will be fetched
            kwargs["version"] = version
        request_body = json.dumps(kwargs)
        response_dto = self._call_endpoint(config.GetModelVersionByName, request_body)
        return ModelVersion.from_proto(response_dto.model_version)

    def get_model_version_by_fqn(
        self,
        fqn: str,
        # unused kwargs
        status: typing.Optional[ArtifactVersionStatus] = None,
    ) -> ModelVersion:
        message = {"fqn": fqn}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetModelVersionByFqn, request_body)
        return ModelVersion.from_dto(response_dto.model_version)

    def update_model_version(
        self,
        version_id: uuid.UUID,
        description: typing.Optional[str] = SENTINEL,
        artifact_metadata: typing.Dict[str, typing.Any] = SENTINEL,
        model_schema: ModelSchema = SENTINEL,
        model_framework: typing.Optional[str] = None,
    ) -> ModelVersion:
        kwargs = dict(description=description, model_framework=model_framework)
        if artifact_metadata is not SENTINEL:
            kwargs["artifact_metadata"] = artifact_metadata
        if model_schema is not SENTINEL:
            kwargs["model_schema"] = model_schema.to_dto()
        kwargs = {k: v for k, v in kwargs.items() if v is not SENTINEL}
        message = config.UpdateModelVersion.request_dto(id=str(version_id), **kwargs)
        request_body = message.json()
        response_dto = self._call_endpoint(config.UpdateModelVersion, request_body)
        return ModelVersion.from_dto(response_dto.model_version)

    def add_features_to_model_version(
        self, version_id: uuid.UUID, features: typing.List[Feature]
    ) -> ModelVersion:
        message = config.AddFeaturesToModelVersion.request_dto(
            id=str(version_id), features=[feature.to_proto() for feature in features]
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.AddFeaturesToModelVersion, request_body)
        return ModelVersion.from_dto(response_dto.model_version)

    # TODO: Verify
    def add_custom_metrics_to_model_version(
        self,
        version_id: uuid.UUID,
        custom_metrics: typing.List[CustomMetric],
    ) -> ModelVersion:
        message = config.AddCustomMetricsToModelVersion(
            id=str(version_id), custom_metrics=custom_metrics.__dict__
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.AddCustomMetricsToModelVersion, request_body)
        return ModelVersion.from_proto(response_dto.model_version)

    def list_artifacts(
        self,
        experiment_id: typing.Union[int, str],
        name: str,
        artifact_types: typing.Optional[typing.List[ArtifactType]] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
        offset: typing.Optional[int] = None,
        run_id: typing.Optional[str] = None,
    ) -> PagedList[Artifact]:
        message = config.ListArtifacts.request_dto(
            experiment_id=str(experiment_id),
            name=name,
            artifact_types=artifact_types,
            max_results=max_results,
            page_token=page_token,
            offset=offset,
            run_id=run_id,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListArtifacts, request_body)
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        # If total is not set, we will see it as 0. We need to convert this to None.
        total = response_dto.total
        return PagedList(
            [Artifact.from_dto(av) for av in response_dto.artifacts],
            token=next_page_token,
            total=total,
        )

    def list_artifact_versions(
        self,
        artifact_id: typing.Optional[uuid.UUID] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
        artifact_types: typing.Optional[ArtifactType] = None,
        run_ids: typing.Optional[typing.List[str]] = None,
        run_steps: typing.Optional[typing.List[str]] = None,
        include_internal_metadata: typing.Optional[bool] = False,
        offset: typing.Optional[int] = None,
        statuses: typing.Optional[ArtifactVersionStatus] = None,
    ) -> PagedList[ArtifactVersion]:
        message = config.ListArtifactVersions.request_dto(
            artifact_id=str(artifact_id) if artifact_id else artifact_id,
            max_results=max_results,
            page_token=page_token,
            artifact_types=artifact_types,
            run_ids=run_ids,
            run_steps=run_steps,
            include_internal_metadata=include_internal_metadata,
            offset=offset,
            statuses=statuses,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListArtifactVersions, request_body)
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        # If total is not set, we will see it as 0. We need to convert this to None.
        total = response_dto.total
        return PagedList(
            [ArtifactVersion.from_dto(av) for av in response_dto.artifact_versions],
            token=next_page_token,
            total=total,
        )

    def list_models(
        self,
        experiment_id: typing.Union[int, str],
        name: str,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
        offset: typing.Optional[int] = None,
        monitoring_enabled_only: typing.Optional[bool] = False,
    ) -> PagedList[Model]:
        message = config.ListModel.request_dto(
            experiment_id=str(experiment_id),
            name=name,
            max_results=max_results,
            page_token=page_token,
            offset=offset,
            monitoring_enabled_only=monitoring_enabled_only,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListModel, request_body)
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        # If total is not set, we will see it as 0. We need to convert this to None.
        total = response_dto.total
        return PagedList(
            [Model.from_dto(m) for m in response_dto.models],
            token=next_page_token,
            total=total,
        )

    def list_model_versions(
        self,
        model_id: typing.Optional[uuid.UUID] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
        statuses: typing.Optional[ArtifactVersionStatus] = None,
        offset: typing.Optional[int] = None,
        run_ids: typing.Optional[typing.List[str]] = None,
    ) -> PagedList[ModelVersion]:
        message = config.ListModelVersion(
            model_id=str(model_id) if model_id else model_id,
            max_results=max_results,
            page_token=page_token,
            offset=offset,
            run_ids=run_ids,
            statuses=statuses,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListModelVersion, request_body)
        # If next_page_token is not set, we will see it as "". We need to convert this to None.
        next_page_token = response_dto.next_page_token
        # If total is not set, we will see it as 0. We need to convert this to None.
        total = response_dto.total
        return PagedList(
            [ModelVersion.from_dto(mv) for mv in response_dto.model_versions],
            token=next_page_token,
            total=total,
        )

    def create_multipart_upload(
        self, artifact_version_id: uuid.UUID, path: str, num_parts: int
    ) -> MultiPartUpload:
        message = config.CreateMultiPartUpload.request_dto(
            artifact_version_id=str(artifact_version_id), path=path, num_parts=num_parts
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateMultiPartUpload, request_body)
        return MultiPartUpload.from_dto(response_dto.multipart_upload)

    def authorize_user_for_model(
        self,
        model_id: uuid.UUID,
        role: typing.Text,
    ) -> None:
        message = config.AuthorizeUserForModel.request_dto(id=str(model_id), role=role)
        request_body = message.json()
        self._call_endpoint(config.AuthorizeUserForModel, request_body)

    def authorize_user_for_model_version(self, version_id: uuid.UUID, role: typing.Text) -> None:
        message = config.AuthorizeUserForModelVersion.request_dto(id=str(version_id), role=role)
        request_body = message.json()
        self._call_endpoint(config.AuthorizeUserForModelVersion, request_body)

    def create_artifact(
        self,
        experiment_id: typing.Union[str, int],
        name: str,
        artifact_type: ArtifactType,
    ) -> uuid.UUID:
        message = config.CreateArtifact.request_dto(
            experiment_id=str(experiment_id), name=name, artifact_type=artifact_type
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateArtifact, request_body)
        return uuid.UUID(response_dto.id)

    def create_dataset(
        self,
        name: str,
        experiment_id: int,
        description: typing.Optional[str] = None,
        dataset_metadata: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ) -> Dataset:
        message = config.CreateDataset.request_dto(
            experiment_id=str(experiment_id),
            name=name,
            description=description,
            dataset_metadata=dataset_metadata,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateDataset, request_body)
        return Dataset.from_dto(response_dto.dataset)

    def get_dataset(
        self,
        id: str,
    ) -> Dataset:
        message = {"id": id}

        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetDataset, request_body)
        return Dataset.from_dto(response_dto.dataset)

    def get_dataset_by_fqn(
        self,
        fqn: str,
    ) -> Dataset:
        message = {"fqn": fqn}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetDatasetByFqn, request_body)
        return response_dto.dataset

    def get_signed_urls_for_dataset_read(
        self, fqn: str, paths: typing.List[str]
    ) -> typing.List[SignedURL]:
        message = config.GetSignedUrlsDatasetRead.request_dto(dataset_fqn=fqn, paths=paths)
        request_body = message.json()
        response_dto = self._call_endpoint(config.GetSignedUrlsDatasetRead, request_body)
        return [SignedURL.from_dto(s) for s in response_dto.signed_urls]

    def get_signed_urls_for_dataset_write(
        self, fqn: str, paths: typing.List[str]
    ) -> typing.List[SignedURL]:
        message = {"paths": paths, "dataset_fqn": fqn}
        request_body = json.dumps(message)
        response_dto = self._call_endpoint(config.GetSignedUrlsForDatasetWrite, request_body)
        return [SignedURL.from_dto(s) for s in response_dto.signed_urls]

    def list_files_for_dataset(
        self,
        fqn: str,
        path: typing.Optional[str] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
    ) -> PagedList[FileInfo]:
        message = config.ListFilesForDataset.request_dto(
            dataset_fqn=fqn, path=path, max_results=max_results, page_token=page_token
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListFilesForDataset, request_body)

        return PagedList(
            [FileInfo.from_dto(f) for f in response_dto.files],
            token=response_dto.next_page_token,
        )

    def create_multipart_upload_for_dataset(
        self, fqn: str, path: str, num_parts: int
    ) -> MultiPartUpload:
        message = config.CreateMultipartUploadForDataset.request_dto(
            dataset_fqn=fqn, path=path, num_parts=num_parts
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.CreateMultipartUploadForDataset, request_body)
        return MultiPartUpload.from_dto(response_dto.multipart_upload)

    def list_datasets(
        self,
        experiment_id: typing.Union[int, str],
        name: typing.Optional[str] = None,
        max_results: typing.Optional[int] = None,
        page_token: typing.Optional[str] = None,
        offset: typing.Optional[int] = None,
    ) -> PagedList[Dataset]:
        message = config.ListDatasets.request_dto(
            experiment_id=str(experiment_id),
            name=name,
            max_results=max_results,
            page_token=page_token,
            offset=offset,
        )
        request_body = message.json()
        response_dto = self._call_endpoint(config.ListDatasets, request_body)
        return PagedList(
            [Dataset.from_dto(av) for av in response_dto.datasets],
            token=response_dto.next_page_token,
            total=response_dto.total,
        )

    def update_dataset(
        self,
        fqn: str,
        description: typing.Optional[str] = SENTINEL,
        dataset_metadata: typing.Dict[str, typing.Any] = SENTINEL,
    ) -> Dataset:
        kwargs = dict(description=description)
        if dataset_metadata is not SENTINEL:
            kwargs["dataset_metadata"] = dict_to_proto(dataset_metadata)
        kwargs = {k: v for k, v in kwargs.items() if v is not SENTINEL}
        message = config.UpdateDataset.request_dto(fqn=fqn, **kwargs)
        request_body = message.json()
        response_dto = self._call_endpoint(config.UpdateDataset, request_body)
        return Dataset.from_dto(response_dto.dataset)


class DatabricksRestStore(RestStore):
    """
    Databricks-specific RestStore implementation that provides different fallback
    behavior when hitting the GetExperimentByName REST API fails - in particular, we only
    fall back to ListExperiments when the server responds with ENDPOINT_NOT_FOUND, rather than
    on all internal server errors. This implementation should be deprecated once
    GetExperimentByName is available everywhere.
    """

    def get_experiment_by_name(self, experiment_name):
        try:
            req_body = json.dumps({"experiment_name": experiment_name})
            response_dto = self._call_endpoint(config.GetExperimentByName, req_body)
            return Experiment.from_dto(response_dto.experiment)
        except MlflowException as e:
            if e.error_code == databricks_pb2.ErrorCode.Name(
                databricks_pb2.RESOURCE_DOES_NOT_EXIST
            ):
                return None
            elif e.error_code == databricks_pb2.ErrorCode.Name(databricks_pb2.ENDPOINT_NOT_FOUND):
                # Fall back to using ListExperiments-based implementation.
                for experiments in self._paginate_list_experiments(ViewType.ALL):
                    for experiment in experiments:
                        if experiment.name == experiment_name:
                            return experiment
                return None
            raise e

    def _paginate_list_experiments(self, view_type):
        page_token = None
        while True:
            experiments = self.list_experiments(view_type=view_type, page_token=page_token)
            yield experiments

            if not experiments.token:
                break
            page_token = experiments.token
