import os
from dotenv import load_dotenv
import pymysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_db_config():
    """Get database configuration based on environment."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'database': os.getenv('DB_NAME', 'email_campaign_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

def get_db_connection():
    """Get a database connection."""
    try:
        config = get_db_config()
        connection = pymysql.connect(**config)
        logger.info("Database connection established successfully")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def release_connection(conn):
    """Release a database connection back to the pool."""
    if connection_pool is not None:
        connection_pool.putconn(conn)

def close_all_connections():
    """Close all database connections."""
    global connection_pool
    if connection_pool is not None:
        connection_pool.closeall()
        connection_pool = None
        logger.info("All database connections closed") 