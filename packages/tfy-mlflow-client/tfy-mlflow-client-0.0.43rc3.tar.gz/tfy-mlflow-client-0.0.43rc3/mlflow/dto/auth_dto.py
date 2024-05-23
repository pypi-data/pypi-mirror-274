from typing import Optional

from mlflow.pydantic_v1 import BaseModel


class GetTenantIdResponseDto(BaseModel):
    tenant_id: Optional[str]
    tenant_name: Optional[str]
    auth_server_url: Optional[str]
