import psycopg
from typing import Tuple, Optional, List

from plum.clients.postgresql.connectors.base_connector import BasePostgresConnector

class PostgresClient:

    def __init__(self, connector: BasePostgresConnector):
        self._connector: BasePostgresConnector = connector

    def _create_connection(self) -> Tuple[psycopg.Connection, Exception]:
        try:
            connection = psycopg.connect(
                conninfo = self._connector.get_psycopg_connection_string(),
                autocommit = False
            )
        except Exception as conn_err:
            return (None, conn_err)
        return (connection, None)

    def _create_bulk_insert_details(self, dict_col: List[dict]) -> Tuple[List[str], List[Tuple]]:
        key_col: List[str] = dict_col[0].keys()
        
        tuple_col: List[Tuple] = []
        for record in dict_col:
            curr_tuple_state = ()
            for key in key_col:
                curr_tuple_state = curr_tuple_state + (record.get(key),)
            tuple_col.append(curr_tuple_state)
        return (key_col, tuple_col)
    

    def bulk_insert(self, table: str, data: List[dict]) -> Optional[Exception]:
        conn, conn_err = self._create_connection()
        if conn_err != None:
            return conn_err
        
        key_col, tuple_col = self._create_bulk_insert_details(dict_col = data)

        cursor: psycopg.Cursor = conn.cursor()

        try:
            with cursor.copy(
                statement = f"COPY {table} ({', '.join(key_col)}) FROM STDIN"
            ) as copy:
                for record in tuple_col:
                    copy.write_row(record)
        except Exception as insert_err:
            conn.close()
            return insert_err
        
        conn.commit()
        conn.close()
        return None