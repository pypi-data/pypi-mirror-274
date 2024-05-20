from abc import ABCMeta, abstractmethod

class BaseS3Connector(metaclass = ABCMeta):

    def __init__(
        self,
        host: str,
        port: int,
        bucket_name: str,
        tls: bool,
        region_name: str = "us-east-1"
    ):
        self.host = host
        self.port = port
        self.bucket_name = bucket_name
        self.tls = tls
        self.region_name = region_name

    def get_endpoint(self) -> str:
        protocol: str = "https" if self.tls else "http"
        return f"{protocol}://{self.host}:{self.port}"