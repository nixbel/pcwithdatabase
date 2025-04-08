from database.user_operations import (
    create_user,
    get_user_by_email,
    get_all_users,
    update_user,
    delete_user,
    create_user_profile,
    get_user_profile
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_user_details(user):
    """Print user details in a formatted way."""
    logger.info(f"""
    User Details:
    ------------
    ID: {user['id']}
    Email: {user['email']}
    First Name: {user.get('first_name', 'N/A')}
    Last Name: {user.get('last_name', 'N/A')}
    Created At: {user['created_at']}
    Updated At: {user.get('updated_at', 'N/A')}
    """)

def print_profile_details(profile):
    """Print profile details in a formatted way."""
    if profile:
        logger.info(f"""
        Profile Details:
        ---------------
        ID: {profile['id']}
        Phone: {profile.get('phone', 'N/A')}
        Address: {profile.get('address', 'N/A')}
        City: {profile.get('city', 'N/A')}
        Country: {profile.get('country', 'N/A')}
        Created At: {profile['created_at']}
        Updated At: {profile.get('updated_at', 'N/A')}
        """)
    else:
        logger.info("No profile found")

def run_demo():
    try:
        # 1. Create a new user
        logger.info("\n=== Creating New User ===")
        new_user = create_user(
            email="john.doe@example.com",
            password="securepassword123",
            first_name="John",
            last_name="Doe"
        )
        print_user_details(new_user)

        # 2. Create user profile
        logger.info("\n=== Creating User Profile ===")
        new_profile = create_user_profile(
            user_id=new_user['id'],
            phone="+1234567890",
            address="123 Main St",
            city="New York",
            country="USA"
        )
        print_profile_details(new_profile)

        # 3. Get user by email
        logger.info("\n=== Retrieving User by Email ===")
        found_user = get_user_by_email("john.doe@example.com")
        print_user_details(found_user)

        # 4. Get user profile
        logger.info("\n=== Retrieving User Profile ===")
        user_profile = get_user_profile(found_user['id'])
        print_profile_details(user_profile)

        # 5. Update user
        logger.info("\n=== Updating User ===")
        updated_user = update_user(
            user_id=found_user['id'],
            first_name="Johnny",
            last_name="Smith"
        )
        print_user_details(updated_user)

        # 6. Get all users
        logger.info("\n=== Retrieving All Users ===")
        all_users = get_all_users()
        for user in all_users:
            print_user_details(user)

        # 7. Delete user (this will also delete the profile due to CASCADE)
        logger.info("\n=== Deleting User ===")
        delete_user(found_user['id'])
        logger.info("User deleted successfully")

    except Exception as e:
        logger.error(f"Error during demo: {e}")

if __name__ == "__main__":
    run_demo() 