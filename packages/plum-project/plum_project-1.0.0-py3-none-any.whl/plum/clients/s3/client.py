from typing import Any, Tuple, List

import boto3
from botocore.client import Config
import botocore.exceptions as boto_errors

from plum.clients.s3.connectors.base_connector import BaseS3Connector

class BucketClientError(Exception):
    def __init__(self, err_msg: str):
        super().__init__(
            f'failed to properly configure connection/query details for storage bucket; {err_msg}'
        )

class BucketConnectionTimeoutError(Exception):
    def __init__(self, err_msg: str):
        super().__init__(
            f'failed to establish connection to storage bucket, timeout reached; {err_msg}'
        )

class ListObjectsNotFoundError(Exception):
    def __init__(self):
        super().__init__('no objects found from storage bucket list operation')

class ObjectNotFoundError(Exception):
    def __init__(self, err_msg: str, resource_path: str):
        super().__init__(
            f'object "{resource_path}" not found in storage bucket; {err_msg}'
        )

class BucketError(Exception):
    def __init__(self, err_msg: str):
        super().__init__(
            f'failed to connect to storage bucket; {err_msg}'
        )

class S3Client:

    def __init__(
            self, 
            connector: BaseS3Connector,
            timeout: int = 5,
            attempts: int = 1
        ):
        self._connector = connector
        self._timeout = timeout
        self._attempts = attempts

    def _create_boto3_client(self) -> Any:
        # Reference to code below here: https://stackoverflow.com/a/48265766
        client_config = Config(
            connect_timeout = self._timeout,
            retries = { 'max_attempts': self._attempts }
        )
        if self._connector.__class__.__name__ == "S3AccessKeyConnector":
            client = boto3.client(
                's3',
                endpoint_url = self._connector.get_endpoint(),
                aws_access_key_id = self._connector.access_key_id,
                aws_secret_access_key = self._connector.access_key_secret,
                region_name = self._connector.region_name,
                config = client_config
            )
            return client
        else:
            return None
    
    def list_objects(self, prefix: str) -> Tuple[List[dict], Exception]:
        """
        Handles the listing of all objects under a certain directory
        in the bucket.
        """
        client = self._create_boto3_client()

        try:
            list_result = client.list_objects_v2(
                Bucket = self._connector.bucket_name,
                Prefix = prefix
            )

        except boto_errors.ConnectTimeoutError as conn_timeout_err:
            return (None, BucketConnectionTimeoutError(conn_timeout_err.args[0]))
        
        except boto_errors.ClientError as client_err:
            return (None, BucketClientError(client_err.args[0]))
        
        except Exception as list_err:
            return (None, BucketError(list_err.args[0]))
        
        if list_result.get('Contents') == None:
            return (None, ListObjectsNotFoundError())
        return (list_result.get('Contents'), None)

    def get_object_contents(self, key: str) -> Tuple[bytes, Exception]:
        """
        Handles the reading of target object in the bucket returning
        the whole byte stream.
        """
        client = self._create_boto3_client()

        try:
            file_data = client.get_object(Bucket = self._connector.bucket_name, Key = key)

        except boto_errors.ConnectTimeoutError as conn_timeout_err:
            return (None, BucketConnectionTimeoutError(conn_timeout_err.args[0]))
        
        except boto_errors.ClientError as client_err:
            if client_err.response.get('Error').get('Code').upper() == 'NOSUCHKEY':
                resource_path: str = client_err.response.get('Error').get('Resource')
                return (None, ObjectNotFoundError(client_err.args[0], resource_path))
            return (None, BucketClientError(client_err.args[0]))
        
        except Exception as read_file_err:
            return (None, BucketError(read_file_err.args[0]))
        
        contents = file_data['Body'].read()
        return (contents, None)