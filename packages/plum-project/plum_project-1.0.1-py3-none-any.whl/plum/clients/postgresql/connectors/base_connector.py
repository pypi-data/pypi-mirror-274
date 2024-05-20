from abc import ABCMeta, abstractmethod

class BasePostgresConnector(metaclass = ABCMeta):
    def __init__(
        self,
        host: str,
        port: int,
        database: str
    ):
        self._host: str = host
        self._port: int = port
        self._database: str = database
    
    @abstractmethod
    def get_psycopg_connection_string(self) -> str:
        pass