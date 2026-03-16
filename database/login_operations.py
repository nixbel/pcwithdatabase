from database.config import get_db_connection, release_connection
import logging
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_login_attempts_table():
    """Create the login_attempts table if it doesn't exist."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                timestamp VARCHAR(100) NOT NULL,
                ip_address VARCHAR(45),
                device_fingerprint VARCHAR(255),
                device_type VARCHAR(50),
                browser_info JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_login_attempts_username 
            ON login_attempts(username)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_login_attempts_timestamp 
            ON login_attempts(created_at)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_login_attempts_ip 
            ON login_attempts(ip_address)
        """)
        
        conn.commit()
        logger.info("Login attempts table created successfully!")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating login_attempts table: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def save_login_attempt(username, password, timestamp, ip_address=None, 
                      device_fingerprint=None, device_type=None, browser_info=None):
    """Save a login attempt to the database."""
    conn = None
    try:
        # Ensure table exists
        create_login_attempts_table()
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Parse browser_info if it's a string (JSON)
        if isinstance(browser_info, str):
            try:
                browser_info = json.loads(browser_info)
            except:
                browser_info = None
        
        cursor.execute("""
            INSERT INTO login_attempts 
            (username, password, timestamp, ip_address, device_fingerprint, device_type, browser_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, username, password, timestamp, ip_address, device_fingerprint, 
                     device_type, browser_info, created_at;
        """, (username, password, timestamp, ip_address, device_fingerprint, 
              device_type, json.dumps(browser_info) if browser_info else None))
        
        new_entry = cursor.fetchone()
        conn.commit()
        logger.info(f"Saved login attempt for username: {username}")
        return new_entry
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error saving login attempt: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_all_login_attempts():
    """Retrieve all login attempts from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, username, password, timestamp, ip_address, device_fingerprint, 
                   device_type, browser_info, created_at
            FROM login_attempts
            ORDER BY created_at DESC;
        """)
        
        results = cursor.fetchall()
        
        # Convert results to list of dicts with proper format
        entries = []
        for row in results:
            entry = {
                'id': row['id'],
                'username': row['username'],
                'password': row['password'],
                'timestamp': row['timestamp'],
                'ip_address': row.get('ip_address'),
                'device_fingerprint': row.get('device_fingerprint'),
                'device_type': row.get('device_type'),
                'browser_info': row.get('browser_info'),
                'created_at': row.get('created_at')
            }
            entries.append(entry)
        
        return entries
        
    except Exception as e:
        logger.error(f"Error retrieving login attempts: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_login_attempt_by_id(entry_id):
    """Retrieve a specific login attempt by ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, username, password, timestamp, ip_address, device_fingerprint, 
                   device_type, browser_info, created_at
            FROM login_attempts
            WHERE id = %s;
        """, (entry_id,))
        
        return cursor.fetchone()
        
    except Exception as e:
        logger.error(f"Error retrieving login attempt: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def delete_login_attempt(entry_id):
    """Delete a specific login attempt by ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM login_attempts WHERE id = %s;", (entry_id,))
        conn.commit()
        
        logger.info(f"Deleted login attempt with ID: {entry_id}")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error deleting login attempt: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def delete_all_login_attempts():
    """Delete all login attempts from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("TRUNCATE TABLE login_attempts RESTART IDENTITY CASCADE;")
        conn.commit()
        
        logger.info("Deleted all login attempts")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error deleting all login attempts: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_last_modified_timestamp():
    """Get the timestamp of the most recent login attempt."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT timestamp, created_at
            FROM login_attempts
            ORDER BY created_at DESC
            LIMIT 1;
        """)
        
        result = cursor.fetchone()
        if result:
            # Return the timestamp field (which has PHT format)
            return result['timestamp']
        else:
            # No entries, return current time with PHT
            from datetime import datetime, timedelta
            now = datetime.now()
            adjusted_time = now + timedelta(hours=8)
            return adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
        
    except Exception as e:
        logger.error(f"Error getting last modified timestamp: {e}")
        # Return current time with PHT as fallback
        from datetime import datetime, timedelta
        now = datetime.now()
        adjusted_time = now + timedelta(hours=8)
        return adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
    finally:
        if conn:
            release_connection(conn)

def get_login_attempts_count():
    """Get the total count of login attempts."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM login_attempts;")
        result = cursor.fetchone()
        return result[0] if result else 0
        
    except Exception as e:
        logger.error(f"Error getting login attempts count: {e}")
        return 0
    finally:
        if conn:
            release_connection(conn)
