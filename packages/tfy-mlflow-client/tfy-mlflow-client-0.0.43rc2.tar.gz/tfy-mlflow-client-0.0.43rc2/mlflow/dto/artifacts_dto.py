from typing import List, Optional

from mlflow.dto.mlfoundry_artifacts_dto import FileInfoDto
from mlflow.pydantic_v1 import BaseModel


class ListArtifactsResponseDto(BaseModel):
    root_uri: Optional[str]
    files: List[FileInfoDto]
    next_page_token: Optional[str]
