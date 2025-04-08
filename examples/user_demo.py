from database.user_operations import (
    create_user,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user
)
import bcrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def demo_user_operations():
    try:
        # 1. Create a new user
        email = "test@example.com"
        password = "securepassword123"
        password_hash = hash_password(password)
        
        logger.info("Creating new user...")
        new_user = create_user(email, password_hash)
        logger.info(f"Created user: {new_user}")
        
        # 2. Retrieve user by email
        logger.info("\nRetrieving user by email...")
        found_user = get_user_by_email(email)
        logger.info(f"Found user: {found_user}")
        
        # 3. Get all users
        logger.info("\nRetrieving all users...")
        all_users = get_all_users()
        logger.info(f"All users: {all_users}")
        
        # 4. Update user
        logger.info("\nUpdating user...")
        updated_user = update_user(found_user['id'], email="updated@example.com")
        logger.info(f"Updated user: {updated_user}")
        
        # 5. Delete user
        logger.info("\nDeleting user...")
        deleted = delete_user(found_user['id'])
        logger.info(f"User deleted: {deleted}")
        
    except Exception as e:
        logger.error(f"Error during demo: {e}")

if __name__ == "__main__":
    demo_user_operations() 