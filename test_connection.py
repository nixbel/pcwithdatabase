import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection with detailed error reporting."""
    conn = None
    try:
        # Get database configuration
        db_config = {
            'host': os.getenv('RENDER_DB_HOST'),
            'port': os.getenv('RENDER_DB_PORT'),
            'database': os.getenv('RENDER_DB_NAME'),
            'user': os.getenv('RENDER_DB_USER'),
            'password': os.getenv('RENDER_DB_PASSWORD'),
            'sslmode': 'require'
        }
        
        # Log configuration (without password)
        logger.info(f"Attempting to connect to: {db_config['host']}:{db_config['port']}")
        logger.info(f"Database: {db_config['database']}")
        logger.info(f"User: {db_config['user']}")
        
        # Try to connect
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        logger.info(f"Successfully connected to PostgreSQL: {version}")
        
        # Test database access
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        logger.info(f"Connected to database: {db_name}")
        
        return True
        
    except psycopg2.OperationalError as e:
        logger.error(f"Connection failed: {str(e)}")
        if "password authentication failed" in str(e):
            logger.error("Password authentication failed. Please check your credentials.")
        elif "could not connect to server" in str(e):
            logger.error("Could not connect to server. Please check:")
            logger.error("1. Server is running")
            logger.error("2. Host and port are correct")
            logger.error("3. Firewall settings allow the connection")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False
    finally:
        if conn:
            conn.close()
            logger.info("Connection closed")

if __name__ == "__main__":
    print("Testing database connection...")
    success = test_connection()
    if success:
        print("Connection successful!")
    else:
        print("Connection failed. Check the logs above for details.") 