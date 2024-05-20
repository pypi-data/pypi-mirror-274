from plum.clients.postgresql.connectors.base_connector import BasePostgresConnector

class PostgresSqlLoginConnector(BasePostgresConnector):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str
    ):
        super().__init__(host = host, port = port, database = database)
        self._username: str = username
        self._password: str = password
    
    def get_psycopg_connection_string(self) -> str:
        return f'host={self._host} dbname={self._database} user={self._username} password={self._password} port={self._port}'