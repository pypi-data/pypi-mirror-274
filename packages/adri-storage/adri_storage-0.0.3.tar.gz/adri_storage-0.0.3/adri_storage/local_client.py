import hashlib
import hmac
import os
import tempfile
from typing import Dict, Optional
from .client import Client
import requests
import json
import base64
import uuid
from pathlib import Path
from shutil import copyfileobj


class InvalidParamException(Exception):
    pass

class InvalidPolicyException(Exception):
    pass

class LocalFileSystem(Client):

    def __init__(self, bucket_name: str, local_fs_secret_key: str, local_fs_secured_url: str):
        self.bucket_name = bucket_name
        self.secret_key = local_fs_secret_key
        self.secured_url = local_fs_secured_url

    def put_object_from_url(self, bucket: str, key: str, url: str, temp_directory: str) -> str:
        local_file_uri = os.path.join(temp_directory, key)
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(local_file_uri, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
            try:
                self.post_file(bucket, key, local_file_uri)
                final_url = self.get_final_url(bucket, key)
            finally:
                os.remove(local_file_uri)

            return final_url
        else:
            raise IOError(f"Failed to download file from {url}. Status code: {response.status_code}")
        
    def check_file(self, path: str) -> str:
        if not os.path.isfile(path):
            raise ValueError(f"Specified path {path} is not a normal file")
        return path
    
    def get_security_header(self) -> Dict[str, str]:
        return {"x-auth-secret-key": self.secret_key}
        
    def post_file(self, bucket: str, key: str, file_path: str):
        url = f"{self.secured_url}/objects"
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'multipart/form-data')}
            data = {'bucket': bucket, 'key': key}
            headers = {'x-auth-secret-key': self.secret_key}
            response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code != 204:
            raise IOError("Failed to post object.")

    def get_final_url(self, bucket: str, key: str) -> str:
        return f"{self.secured_url}/objects/{bucket}/{key}"
    
    def put_object(self, bucket_name: str, key: str, content: Optional[str] = None) -> str:
        if content is None:
            return self.put_object_without_content(bucket_name, key)
        else:
            return self.put_object_with_content(bucket_name, key, content)
    
    def put_object_without_content(self, bucket_name: str, key: str) -> str:
        url = f"{self.secured_url}/objects/{bucket_name}/{key}"
        suffix = "/"
        if str(key).endswith(suffix) and not url.endswith(suffix):
            url += suffix

        headers = self.get_security_header()
        response = requests.post(url, headers=headers)
        
        if response.status_code != 204:
            raise IOError("Failed to post object.")
        return key
    
    def put_object_with_content(self, bucket_name: str, key: str, content: str) -> str:
        if isinstance(content, bytes):
            content_bytes = base64.b64decode(content, validate=True)
        else:
            raise InvalidParamException("Content must be a base64 encoded string.")

        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            temp_file.write(content_bytes)
        try:
            self.post_file(bucket_name, key, temp_file.name)
        finally:
            os.unlink(temp_file.name)
        return key
    
    def put_object_request(self, bucket_name: str, key: str, local_file_path: str) -> str:
        if not os.path.isfile(local_file_path):
            raise ValueError(f"Specified path {local_file_path} is not a normal file")
        self.post_file(bucket_name, key, local_file_path)
        return key
    
    def delete_object(self, bucket_name: str, key: str):
        url = f"{self.secured_url}/objects/{bucket_name}/{key}"
        
        headers = self.get_security_header()

        response = requests.delete(url, headers=headers)
        
        if response.status_code != 204:
            raise IOError("Failed to delete object")
        
    def get_file_stream(self, bucket_name: str, key: str):
        url = f"{self.secured_url}/objects/{bucket_name}/{key}"
        
        headers = self.get_security_header()
        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code != 200:
            raise IOError("Failed to get input stream")
        else:
            return response.raw
        
    def get_file_content(self, bucket_name: str, key: str) -> str:
        stream = self.get_file_stream(bucket_name, key)
        
        content = stream.read()
        
        stream.close()
        
        return content.decode('utf-8')
    
    def copy_object(self, source_bucket_name: str, source_key: str, destination_bucket_name: str, destination_key: str) -> str:
        copy_object_request = {
            "sourceBucket": source_bucket_name,
            "sourceKey": source_key,
            "destBucket": destination_bucket_name,
            "destKey": destination_key
        }

        json_copy_object_request = json.dumps(copy_object_request, separators=(',', ':'))

        url = f"{self.secured_url}/objects/copied"

        response = requests.put(url, data=json_copy_object_request, headers=self.get_security_header())

        if response.status_code != 204:
            raise IOError("Failed to copy object")
        else:
            return self.get_final_url(destination_bucket_name, destination_key)
        
    def calculate_signature(self, secret_key: str, date: str, service_name: str, encrypted_policy: str) -> Optional[str]:
        try:
            signing_key = self.get_signature_key(secret_key, date, service_name)
            hashed = hmac.new(signing_key, encrypted_policy.encode(), hashlib.sha256)
            return hashed.hexdigest()
        except Exception as e:
            print(e)
            return None

    def get_signature_key(self, key: str, date_stamp: str, service_name: str) -> bytes:
        k_secret = ('AWS4' + key).encode('utf-8')
        k_date = hmac.new(k_secret, date_stamp.encode('utf-8'), hashlib.sha256).digest()
        k_service = hmac.new(k_date, service_name.encode('utf-8'), hashlib.sha256).digest()
        k_signing = hmac.new(k_service, b'aws4_request', hashlib.sha256).digest()
        return k_signing
    
    def bytes_to_hex(self, bytes: bytes) -> str:
        hex_string = []
        for byte in bytes:
            hex_s = format(byte & 0xFF, '02x')
            hex_string.append(hex_s)
        return ''.join(hex_string)
    
    def download_temp_file(self, bucket: str, key: str, *path_components: str) -> Path:
        input_stream = self.get_file_stream(bucket, key)
        
        try:
            temp_dir = Path(tempfile.gettempdir(), *path_components)
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            temp_file = temp_dir / f"{uuid.uuid4()}.{key.split('.')[-1]}"
            
            with open(temp_file, 'wb') as out_file:
                copyfileobj(input_stream, out_file)
            
            return temp_file

        except Exception as e:
            raise IOError(f"Failed to download temp file: {e}")

        finally:
            input_stream.close()
