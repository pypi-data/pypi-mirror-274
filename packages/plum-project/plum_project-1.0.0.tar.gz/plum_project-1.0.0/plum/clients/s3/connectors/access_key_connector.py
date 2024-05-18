from plum.clients.s3.connectors.base_connector import BaseS3Connector

class S3AccessKeyConnector(BaseS3Connector):

    def __init__(
        self,
        host: str,
        port: int,
        bucket_name: str,
        tls: bool,
        access_key_id: str,
        access_key_secret: str,
        region_name: str = "us-east-1",
    ):
        super().__init__(
              host = host,
              port = port,
              bucket_name = bucket_name,
              tls = tls,
              region_name = region_name
         )
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret