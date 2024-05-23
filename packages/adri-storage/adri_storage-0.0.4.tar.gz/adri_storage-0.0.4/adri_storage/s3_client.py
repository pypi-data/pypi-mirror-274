import base64
import os
import boto3
from typing import Optional, IO
from pathlib import Path
import tempfile
import uuid
import requests
from .client import Client
import tempfile
from pathlib import Path
from botocore.exceptions import ClientError

class S3FileSystem(Client):

    def __init__(self, bucket_name: str, aws_access_key_id: Optional[str] = None, aws_secret_access_key: Optional[str] = None, region_name: Optional[str] = None):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
    
    def put_object_from_url(self, bucket: str, key: str, url: str, temp_directory: str) -> str:
        local_file_uri = os.path.join(temp_directory, key)
        
        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise IOError(f"Failed to download file from {url}. Status code: {response.status_code}")

            with open(local_file_uri, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)

            self.post_file(bucket, key, local_file_uri)

            final_url = self.get_final_url(bucket, key)

            return final_url
        
        finally:
            os.remove(local_file_uri)

    def post_file(self, bucket: str, key: str, file_path: str) -> None:
        try:
            self.s3.upload_file(file_path, bucket, key)
        except ClientError as e:
            raise IOError(f"Failed to post object: {e}")

    def get_final_url(self, bucket: str, key: str) -> str:
        return f"{self.s3.meta.endpoint_url}/{bucket}/{key}"
    
    def put_object(self, bucket_name: str, key: str, content: Optional[str] = None) -> str:
        if content is None:
            return self.put_object_without_content(bucket_name, key)
        else:
            return self.put_object_with_content(bucket_name, key, content)

    def put_object_without_content(self, bucket_name: str, key: str) -> str:
        try:
            self.s3.put_object(Bucket=bucket_name, Key=key)
            return key
        except ClientError as e:
            raise IOError(f"Failed to put object without content: {e}")

    def put_object_with_content(self, bucket_name: str, key: str, content: str) -> str:
        try:
            content_bytes = base64.b64decode(content, validate=True)
            with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                temp_file.write(content_bytes)
            self.post_file(bucket_name, key, temp_file.name)
            return key
        except (ValueError, TypeError, ClientError) as e:
            raise IOError(f"Failed to put object with content: {e}")
        finally:
            os.unlink(temp_file.name)

    def put_object_request(self, bucket_name: str, key: str, local_file_path: str) -> str:
        try:
            if not os.path.isfile(local_file_path):
                raise ValueError(f"Specified path {local_file_path} is not a normal file")
            self.post_file(bucket_name, key, local_file_path)
            return key
        except (ValueError, ClientError) as e:
            raise IOError(f"Failed to put object request: {e}")

    def delete_object(self, bucket: str, key: str) -> None:
        self.s3.delete_object(Bucket=bucket, Key=key)

    def get_file_stream(self, bucket: str, key: str) -> IO[bytes]:
        obj = self.s3.get_object(Bucket=bucket, Key=key)
        return obj['Body']

    def get_file_content(self, bucket: str, key: str) -> str:
        obj = self.s3.get_object(Bucket=bucket, Key=key)
        return obj['Body'].read().decode('utf-8')

    def copy_object(self, source_bucket: str, source_key: str, dest_bucket: str, dest_key: str) -> str:
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        self.s3.copy_object(CopySource=copy_source, Bucket=dest_bucket, Key=dest_key)
        return f"{self.s3.meta.endpoint_url}/{dest_bucket}/{dest_key}"

    def download_temp_file(self, bucket: str, key: str, *options: str) -> Path:
        try:
            temp_dir = Path(tempfile.gettempdir(), *options)
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            temp_file = temp_dir / f"{uuid.uuid4()}.{key.split('.')[-1]}"
            
            self.s3.download_file(bucket, key, str(temp_file))
            
            return temp_file

        except Exception as e:
            raise IOError(f"Failed to download temp file: {e}")


