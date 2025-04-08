import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection pool
connection_pool = None

def get_db_config():
    """Get database configuration based on environment."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'mydatabase'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
    }

def init_connection_pool():
    """Initialize the connection pool."""
    global connection_pool
    try:
        config = get_db_config()
        connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=20,
            **config,
            cursor_factory=RealDictCursor
        )
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise

def get_db_connection():
    """Get a database connection from the pool."""
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

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