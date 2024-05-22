from mlflow.dto.mlfoundry_artifacts_dto import SignedURLDto
from mlflow.pydantic_v1 import BaseModel


class SignedURL(BaseModel):
    path: str
    url: str

    def to_dto(self) -> SignedURLDto:
        return SignedURLDto(path=self.path, signed_url=self.url)

    @classmethod
    def from_dto(cls, dto):
        return cls(path=dto.path, url=dto.signed_url)
