import pymysql
from .config import get_db_config
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        """Get a new database connection."""
        try:
            config = get_db_config()
            conn = pymysql.connect(**config)
            logger.info("Database connection established")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def return_connection(self, conn):
        """Close the connection."""
        if conn:
            try:
                conn.close()
                logger.info("Database connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {e}")