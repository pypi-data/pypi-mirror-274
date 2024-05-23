from typing import List, Optional

from mlflow.dto import mlfoundry_artifacts_dto as mlfa_dto
from mlflow.entities.mlfoundry_artifacts.enums import MultiPartUploadStorageProvider
from mlflow.entities.signed_url import SignedURL
from mlflow.pydantic_v1 import BaseModel


class MultiPartUpload(BaseModel):
    class Config:
        allow_mutation = False

    storage_provider: MultiPartUploadStorageProvider
    part_signed_urls: List[SignedURL]
    s3_compatible_upload_id: Optional[str] = None
    azure_blob_block_ids: Optional[List[str]] = None
    finalize_signed_url: SignedURL

    def to_dto(self) -> mlfa_dto.MultiPartUploadDto:
        mpu_dto = mlfa_dto.MultiPartUploadDto(
            s3_compatible_upload_id=self.s3_compatible_upload_id or "",
            storage_provider=self.storage_provider,
            finalize_signed_url=self.finalize_signed_url.to_dto(),
            part_signed_urls=[signed_url.to_dto() for signed_url in self.part_signed_urls],
            azure_blob_block_ids=self.azure_blob_block_ids,
        )
        return mpu_dto

    @classmethod
    def from_dto(cls, dto):
        return cls(
            storage_provider=dto.storage_provider,
            part_signed_urls=[SignedURL.from_dto(su) for su in dto.part_signed_urls],
            s3_compatible_upload_id=dto.s3_compatible_upload_id,
            azure_blob_block_ids=dto.azure_blob_block_ids,
            finalize_signed_url=SignedURL.from_dto(dto.finalize_signed_url),
        )
