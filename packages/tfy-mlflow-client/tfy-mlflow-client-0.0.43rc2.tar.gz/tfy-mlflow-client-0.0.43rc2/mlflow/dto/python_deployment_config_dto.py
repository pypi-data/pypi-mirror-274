from typing import Any, Dict, Optional

from mlflow.pydantic_v1 import BaseModel


class CreatePythonDeploymentConfigRequestDto(BaseModel):
    workspace_fqn: Optional[str]
    deployment_config: Optional[Dict[str, Any]]


class CreatePythonDeploymentConfigResponseDto(BaseModel):
    deploy_file_content: Optional[str]
