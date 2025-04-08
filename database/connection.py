import psycopg2
from psycopg2 import pool
from .config import DB_CONFIG, POOL_CONFIG

class DatabaseConnection:
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def initialize_pool(self):
        if self._connection_pool is None:
            try:
                self._connection_pool = pool.ThreadedConnectionPool(
                    minconn=POOL_CONFIG['minconn'],
                    maxconn=POOL_CONFIG['maxconn'],
                    **DB_CONFIG
                )
            except Exception as e:
                print(f"Error creating connection pool: {e}")
                raise

    def get_connection(self):
        if self._connection_pool is None:
            self.initialize_pool()
        return self._connection_pool.getconn()

    def return_connection(self, conn):
        if self._connection_pool is not None:
            self._connection_pool.putconn(conn)

    def close_all_connections(self):
        if self._connection_pool is not None:
            self._connection_pool.closeall()
            self._connection_pool = None 