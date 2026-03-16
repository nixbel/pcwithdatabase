"""
Quick Data Viewer - View all data from the database
Run this to see all login attempts recorded in the database
"""

import sys
import os
from tabulate import tabulate
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.login_operations import get_all_login_attempts
    from database.init_db import init_db
    from database.login_operations import create_login_attempts_table
    
    print("=" * 80)
    print("DATABASE DATA VIEWER")
    print("=" * 80)
    print()
    
    # Initialize database tables
    print("Initializing database tables...")
    init_db()
    create_login_attempts_table()
    print("✓ Database initialized")
    print()
    
    # Fetch all attempts
    print("Fetching data from database...")
    attempts = get_all_login_attempts()
    
    if not attempts:
        print("No data found in database yet.")
        print("\nTips:")
        print("1. Run the Flask application: python campaign/app.py")
        print("2. Access http://localhost:5000")
        print("3. Submit the form with your data")
        print("4. Run this script again to see the data")
    else:
        print(f"✓ Found {len(attempts)} entries\n")
        
        # Prepare data for table display
        table_data = []
        for attempt in attempts:
            table_data.append([
                attempt.get('id', 'N/A'),
                attempt.get('username', 'N/A')[:20],  # Truncate for readability
                '*' * 8,  # Don't display actual passwords
                attempt.get('timestamp', 'N/A'),
                attempt.get('ip_address', 'N/A'),
                attempt.get('device_type', 'N/A'),
                attempt.get('created_at', 'N/A')
            ])
        
        # Display table
        headers = ['ID', 'Username', 'Password', 'Timestamp', 'IP Address', 'Device Type', 'Created At']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
        print()
        print("=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"Total Entries: {len(attempts)}")
        print(f"Latest Entry: {attempts[0].get('created_at', 'N/A')}" if attempts else "No entries")
        print()
        print("To see more details about a specific entry, modify this script.")
        print("Data security note: Passwords are masked for security in this view.")
    
    print()
    print("=" * 80)
    
except ImportError as e:
    print(f"ERROR: Could not import database modules: {e}")
    print("\nMake sure you're running this from the project root directory:")
    print("python view_data.py")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    print("\nMake sure:")
    print("1. PostgreSQL is running")
    print("2. .env file has correct database credentials")
    print("3. Database 'campaign_db_2mv9' exists")
    sys.exit(1)
