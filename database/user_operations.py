from database.config import get_db_connection, release_connection
import logging
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_user(email, password_hash):
    """Create a new user in the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id, email, created_at;
        """, (email, password_hash))
        
        new_user = cursor.fetchone()
        conn.commit()
        logger.info(f"Created new user with email: {email}")
        return new_user
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating user: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_user_by_email(email):
    """Retrieve a user by email."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, email, created_at, updated_at
            FROM users
            WHERE email = %s;
        """, (email,))
        
        return cursor.fetchone()
        
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_all_users():
    """Retrieve all users."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, email, created_at, updated_at
            FROM users
            ORDER BY created_at DESC;
        """)
        
        return cursor.fetchall()
        
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def update_user(user_id, email=None, password_hash=None):
    """Update user information."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        updates = []
        values = []
        
        if email:
            updates.append("email = %s")
            values.append(email)
        if password_hash:
            updates.append("password_hash = %s")
            values.append(password_hash)
            
        if not updates:
            return None
            
        values.append(user_id)
        
        query = f"""
            UPDATE users 
            SET {", ".join(updates)}
            WHERE id = %s
            RETURNING id, email, updated_at;
        """
        
        cursor.execute(query, tuple(values))
        updated_user = cursor.fetchone()
        conn.commit()
        
        return updated_user
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error updating user: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def delete_user(user_id):
    """Delete a user."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error deleting user: {e}")
        raise
    finally:
        if conn:
            release_connection(conn) 