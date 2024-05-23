from abc import ABC, abstractmethod
from typing import Optional

class Client(ABC):

    @abstractmethod
    def put_object_from_url(self, bucket: str, key: str, url: str, region: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def put_object(self, bucket: str, key: str, content: str) -> str:
        pass

    @abstractmethod
    def put_object(self, bucket: str, key: str) -> str:
        pass

    @abstractmethod
    def put_object_request(self, bucket: str, key: str, request: str) -> str:
        pass

    @abstractmethod
    def delete_object(self, bucket: str, key: str) -> None:
        pass

    @abstractmethod
    def get_file_stream(self, bucket: str, key: str):
        pass

    @abstractmethod
    def get_file_content(self, bucket: str, key: str) -> str:
        pass

    @abstractmethod
    def copy_object(self, source_bucket: str, source_key: str, dest_bucket: str, dest_key: str) -> str:
        pass

    @abstractmethod
    def download_temp_file(self, bucket: str, key: str, *options: str) -> str:
        pass
