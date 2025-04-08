import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize connection pool
connection_pool = None

def get_db_config():
    """Get database configuration based on environment."""
    if os.getenv('FLASK_ENV') == 'production':
        # Use Render configuration
        return {
            'host': os.getenv('RENDER_DB_HOST'),
            'port': os.getenv('RENDER_DB_PORT'),
            'database': os.getenv('RENDER_DB_NAME'),
            'user': os.getenv('RENDER_DB_USER'),
            'password': os.getenv('RENDER_DB_PASSWORD'),
            'sslmode': 'require'
        }
    else:
        # Use local configuration
        return {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }

def init_connection_pool():
    """Initialize the connection pool."""
    global connection_pool
    try:
        if os.getenv('FLASK_ENV') == 'production':
            # Use DATABASE_URL for Render
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable is not set")
            
            connection_pool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                dsn=database_url,
                cursor_factory=RealDictCursor,
                sslmode='require'
            )
        else:
            # Use local configuration
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
    global connection_pool
    try:
        if connection_pool is None:
            init_connection_pool()
        
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        logger.error(f"Error getting database connection: {e}")
        raise

def release_connection(conn):
    """Release a connection back to the pool."""
    try:
        if connection_pool and conn:
            connection_pool.putconn(conn)
    except Exception as e:
        logger.error(f"Error releasing database connection: {e}")

def close_all_connections():
    """Close all connections in the pool."""
    global connection_pool
    try:
        if connection_pool:
            connection_pool.closeall()
            connection_pool = None
            logger.info("All database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}") 