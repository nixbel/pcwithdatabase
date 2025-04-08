import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'phishing_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Connection pool settings
POOL_CONFIG = {
    'minconn': 1,
    'maxconn': 20,
    'connect_timeout': 30
}

def get_db_connection():
    """Create and return a database connection."""
    try:
        # Get the database URL from environment (set by Render)
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
            
        # Parse the database URL
        parsed_url = urlparse(database_url)
        
        # Create connection using the URL
        conn = psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor,
            sslmode='require'  # Enable SSL for Render
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise 