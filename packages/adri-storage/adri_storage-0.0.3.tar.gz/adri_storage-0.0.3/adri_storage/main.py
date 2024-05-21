from .local_client import LocalFileSystem
from .s3_client import S3FileSystem
from .client import Client
from .client_enums import FileSystemType

def get_filesystem(fs_type:FileSystemType, **kwargs) -> Client:
    """
    Get an instance of a file system client based on the specified file system type.

    Parameters:
        fs_type (FileSystemType): The type of file system client to instantiate.
            Supported types are FileSystemType.LOCAL and FileSystemType.S3.

        kwargs: Additional keyword arguments specific to the file system type.

            For FileSystemType.LOCAL:
                - bucket_name (str): The name of the bucket or directory.
                - secret_key (str): The secret key for authentication.
                - secured_url (str): The secured URL for accessing the file system.

            For FileSystemType.S3:
                - bucket_name (str): The name of the S3 bucket.
                - access_key (str): The AWS access key ID for authentication.
                - secret_key (str): The AWS secret access key for authentication.
                - region_name (str): The AWS region where the S3 bucket is located.

    Returns:
        Client: An instance of the file system client.

    Raises:
        ValueError: If an unsupported file system type is specified.
    """
    if fs_type == FileSystemType.LOCAL:
        return LocalFileSystem(
            bucket_name=kwargs.get("bucket_name"),
            local_fs_secret_key=kwargs.get('secret_key'),
            local_fs_secured_url=kwargs.get('secured_url')
        )
    elif fs_type == FileSystemType.S3:
        return S3FileSystem(
            bucket_name=kwargs.get('bucket_name'),
            aws_access_key_id=kwargs.get('access_key'),
            aws_secret_access_key=kwargs.get('secret_key'),
            region_name=kwargs.get('region_name')
        )
    else:
        raise ValueError(f"Unsupported file system type: {fs_type}")
