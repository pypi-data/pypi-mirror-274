from mlflow.dto.mlfoundry_artifacts_dto import FileInfoDto
from mlflow.entities._mlflow_object import _MLflowObject


class FileInfo(_MLflowObject):
    """
    Metadata about a file or directory.
    """

    def __init__(self, path, is_dir, file_size, signed_url=None):
        self._path = path
        self._is_dir = is_dir
        self._bytes = file_size
        self._signed_url = signed_url

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def path(self):
        """String path of the file or directory."""
        return self._path

    @property
    def is_dir(self):
        """Whether the FileInfo corresponds to a directory."""
        return self._is_dir

    @property
    def file_size(self):
        """Size of the file or directory. If the FileInfo is a directory, returns None."""
        return self._bytes

    @property
    def signed_url(self):
        """Signed url to read the file. If the FileInfo is a directory or comes from non s3 store, returns None"""
        return self._signed_url

    def to_dto(self) -> FileInfoDto:
        dto = FileInfoDto(path=self.path, is_dir=self.is_dir)
        if self.file_size:
            dto.file_size = self.file_size
        if self.signed_url:
            dto.signed_url = self.signed_url
        return dto

    @classmethod
    def from_dto(cls, dto):
        signed_url = dto.signed_url
        return cls(path=dto.path, is_dir=dto.is_dir, file_size=dto.file_size, signed_url=signed_url)
