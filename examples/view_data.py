from database.user_operations import get_all_users, get_user_by_email
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def view_database_data():
    try:
        # View all users
        logger.info("\n=== All Users in Database ===")
        all_users = get_all_users()
        for user in all_users:
            logger.info(f"""
            User ID: {user['id']}
            Email: {user['email']}
            Created At: {user['created_at']}
            Updated At: {user['updated_at']}
            -------------------------
            """)
            
        # If you want to view a specific user
        specific_email = input("\nEnter an email to view specific user (or press Enter to skip): ")
        if specific_email:
            user = get_user_by_email(specific_email)
            if user:
                logger.info(f"""
                === Specific User Details ===
                User ID: {user['id']}
                Email: {user['email']}
                Created At: {user['created_at']}
                Updated At: {user['updated_at']}
                """)
            else:
                logger.info(f"No user found with email: {specific_email}")
                
    except Exception as e:
        logger.error(f"Error viewing data: {e}")

if __name__ == "__main__":
    view_database_data() 