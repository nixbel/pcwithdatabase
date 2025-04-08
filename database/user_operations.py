from database.config import get_db_connection, release_connection
import logging
from psycopg2.extras import RealDictCursor
import bcrypt
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed_password):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_user(email, password, first_name=None, last_name=None):
    """Create a new user in the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Hash the password
        password_hash = hash_password(password)
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, first_name, last_name, created_at;
        """, (email, password_hash, first_name, last_name))
        
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
            SELECT id, email, first_name, last_name, created_at, updated_at
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
            SELECT id, email, first_name, last_name, created_at, updated_at
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

def update_user(user_id, email=None, password=None, first_name=None, last_name=None):
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
        if password:
            updates.append("password_hash = %s")
            values.append(hash_password(password))
        if first_name:
            updates.append("first_name = %s")
            values.append(first_name)
        if last_name:
            updates.append("last_name = %s")
            values.append(last_name)
            
        if not updates:
            return None
            
        values.append(user_id)
        
        query = f"""
            UPDATE users 
            SET {", ".join(updates)}
            WHERE id = %s
            RETURNING id, email, first_name, last_name, updated_at;
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

def create_user_profile(user_id, phone=None, address=None, city=None, country=None):
    """Create a user profile."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            INSERT INTO user_profiles (user_id, phone, address, city, country)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, user_id, phone, address, city, country, created_at;
        """, (user_id, phone, address, city, country))
        
        new_profile = cursor.fetchone()
        conn.commit()
        logger.info(f"Created profile for user: {user_id}")
        return new_profile
        
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error creating user profile: {e}")
        raise
    finally:
        if conn:
            release_connection(conn)

def get_user_profile(user_id):
    """Get a user's profile."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, user_id, phone, address, city, country, created_at, updated_at
            FROM user_profiles
            WHERE user_id = %s;
        """, (user_id,))
        
        return cursor.fetchone()
        
    except Exception as e:
        logger.error(f"Error retrieving user profile: {e}")
        raise
    finally:
        if conn:
            release_connection(conn) 