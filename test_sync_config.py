#!/usr/bin/env python3
"""
Test script to verify Cloud-to-Local Sync configuration
Run this before running local_sync.py to ensure everything is working
"""

import requests
import mysql.connector
import json
from datetime import datetime

# Configuration (same as local_sync.py)
CLOUD_URL = "https://campaign-rzp2.onrender.com/api/fetch-entries"
API_KEY = "abcdefghijklmnopnp2025"

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pnp_data'
}

def print_header(title):
    """Print formatted header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")

def test_cloud_connection():
    """Test connection to cloud server"""
    print("🔍 Testing Cloud Server Connection...")
    print(f"   URL: {CLOUD_URL}")
    print(f"   API Key: {API_KEY[:10]}...{API_KEY[-5:]}")
    
    try:
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'last_sync_timestamp': ''
        }
        
        print("   📡 Sending request...")
        response = requests.post(CLOUD_URL, headers=headers, json=payload, timeout=10)
        
        print(f"   ✓ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Cloud server is responding correctly!")
            print(f"   ✓ Available entries: {data.get('count', 0)}")
            print(f"   ✓ Sync timestamp: {data.get('sync_timestamp', 'N/A')}")
            
            if data.get('entries'):
                first_entry = data['entries'][0]
                print("\n   Sample entry fields:")
                for key in first_entry.keys():
                    value = first_entry[key]
                    if isinstance(value, dict):
                        value = f"{{...}} (dict with {len(value)} keys)"
                    print(f"   - {key}: {str(value)[:50]}")
            
            return True
        elif response.status_code == 401:
            print(f"   ✗ Authentication failed!")
            print(f"   ✗ API Key might be incorrect")
            return False
        else:
            print(f"   ✗ Server returned error: {response.status_code}")
            print(f"   ✗ Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ✗ Connection timeout (10 seconds)")
        print(f"   ✗ Cloud server may be unreachable or too slow")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ✗ Connection error: {str(e)[:100]}")
        print(f"   ✗ Cannot reach cloud server. Check URL and network.")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)[:100]}")
        return False

def test_mysql_connection():
    """Test connection to MySQL"""
    print("\n🔍 Testing MySQL Connection...")
    print(f"   Host: {MYSQL_CONFIG['host']}")
    print(f"   User: {MYSQL_CONFIG['user']}")
    print(f"   Database: {MYSQL_CONFIG['database']}")
    
    try:
        print("   📡 Connecting to MySQL...")
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        print("   ✓ MySQL server is accessible!")
        
        # Check if database exists
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE 'pnp_data'")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("   ✓ Database 'pnp_data' exists")
            
            # Check if table exists
            conn_db = mysql.connector.connect(**MYSQL_CONFIG)
            cursor_db = conn_db.cursor()
            cursor_db.execute("SHOW TABLES LIKE 'login_data'")
            table_exists = cursor_db.fetchone()
            
            if table_exists:
                print("   ✓ Table 'login_data' exists")
                
                # Get row count
                cursor_db.execute("SELECT COUNT(*) FROM login_data")
                count = cursor_db.fetchone()[0]
                print(f"   ✓ Table has {count} entries")
            else:
                print("   ⚠ Table 'login_data' not found (will be created on first sync)")
            
            cursor_db.close()
            conn_db.close()
        else:
            print("   ⚠ Database 'pnp_data' not found (will be created on first sync)")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        if err.errno == 2003:
            print(f"   ✗ Cannot connect - MySQL server not running or unreachable")
            print(f"   ✗ Error: {err.msg}")
            print(f"   ℹ Solution: Start MySQL in XAMPP or verify connection settings")
        elif err.errno == 1045:
            print(f"   ✗ Access denied - wrong credentials")
            print(f"   ✗ Error: {err.msg}")
            print(f"   ℹ Solution: Check MySQL username and password")
        else:
            print(f"   ✗ MySQL Error ({err.errno}): {err.msg}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)[:100]}")
        return False

def test_data_fetch():
    """Test fetching and processing data"""
    print("\n🔍 Testing Data Fetch and Processing...")
    
    try:
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {'last_sync_timestamp': ''}
        
        response = requests.post(CLOUD_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code != 200:
            print(f"   ✗ Failed to fetch data: {response.status_code}")
            return False
        
        data = response.json()
        entries = data.get('entries', [])
        
        if not entries:
            print("   ⚠ No entries available to fetch (this is OK for first run)")
            return True
        
        print(f"   ✓ Retrieved {len(entries)} entries")
        
        # Validate first entry
        if entries:
            entry = entries[0]
            required_fields = ['username', 'password', 'timestamp']
            optional_fields = ['ip_address', 'device_fingerprint', 'device_type', 'browser_info']
            
            missing = [f for f in required_fields if f not in entry or not entry[f]]
            if missing:
                print(f"   ⚠ Missing required fields: {missing}")
            else:
                print(f"   ✓ All required fields present")
            
            print(f"   ✓ Sample data:")
            print(f"     - Username: {entry.get('username', 'N/A')}")
            print(f"     - Timestamp: {entry.get('timestamp', 'N/A')}")
            print(f"     - IP Address: {entry.get('ip_address', 'N/A')}")
            print(f"     - Device Type: {entry.get('device_type', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:100]}")
        return False

def run_all_tests():
    """Run all tests"""
    print_header("CLOUD-TO-LOCAL SYNC CONFIGURATION TEST")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "Cloud Connection": test_cloud_connection(),
        "MySQL Connection": test_mysql_connection(),
        "Data Fetch": test_data_fetch()
    }
    
    print_header("TEST RESULTS")
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    all_passed = all(results.values())
    
    if all_passed:
        print("="*70)
        print("✓ All tests passed! You can now run local_sync.py")
        print("="*70)
        return 0
    else:
        print("="*70)
        print("✗ Some tests failed. Please fix the issues above.")
        print("="*70)
        return 1

if __name__ == '__main__':
    exit(run_all_tests())
