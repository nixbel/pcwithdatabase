#!/usr/bin/env python3
"""
Verify MySQL setup for the application
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n" + "="*50)
    print("CHECKING PYTHON PACKAGES")
    print("="*50)
    
    required_packages = {
        'pymysql': 'PyMySQL',
        'flask': 'Flask',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, name in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            missing.append(name)
    
    return len(missing) == 0

def check_mysql_connection():
    """Check if MySQL is running and accessible"""
    print("\n" + "="*50)
    print("CHECKING MYSQL CONNECTION")
    print("="*50)
    
    try:
        import pymysql
        from database.config import get_db_config
        
        config = get_db_config()
        print(f"Attempting to connect to MySQL...")
        print(f"  Host: {config['host']}")
        print(f"  Port: {config['port']}")
        print(f"  User: {config['user']}")
        print(f"  Database: {config['database']}")
        
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✓ MySQL connected successfully!")
        print(f"  MySQL Version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except pymysql.err.OperationalError as e:
        print(f"✗ MySQL connection failed!")
        print(f"  Error: {e}")
        print("\nTroubleshooting steps:")
        print("  1. Make sure XAMPP is running and MySQL is started")
        print("  2. Check if MySQL is running on the correct port (default: 3306)")
        print("  3. Verify credentials in .env file (default: root with no password)")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def check_database_tables():
    """Check if database tables exist"""
    print("\n" + "="*50)
    print("CHECKING DATABASE TABLES")
    print("="*50)
    
    try:
        import pymysql
        from database.config import get_db_config
        
        config = get_db_config()
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Check for tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = %s
        """, (config['database'],))
        
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['login_attempts', 'users', 'campaigns', 'targets', 'results']
        
        for table in required_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' NOT found")
        
        cursor.close()
        conn.close()
        
        return len(tables) >= len(required_tables)
        
    except Exception as e:
        print(f"✗ Error checking tables: {e}")
        return False

def check_env_file():
    """Check if .env file exists and is configured"""
    print("\n" + "="*50)
    print("CHECKING ENVIRONMENT CONFIGURATION")
    print("="*50)
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    if os.path.exists(env_path):
        print(f"✓ .env file found at: {env_path}")
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
            
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '3306')
            db_name = os.getenv('DB_NAME', 'email_campaign_db')
            db_user = os.getenv('DB_USER', 'root')
            
            print(f"  DB_HOST: {db_host}")
            print(f"  DB_PORT: {db_port}")
            print(f"  DB_NAME: {db_name}")
            print(f"  DB_USER: {db_user}")
            return True
        except Exception as e:
            print(f"✗ Error reading .env file: {e}")
            return False
    else:
        print(f"✗ .env file NOT found")
        print(f"  Expected location: {env_path}")
        print("\nCreate .env file with:")
        print("  DB_HOST=localhost")
        print("  DB_PORT=3306")
        print("  DB_NAME=email_campaign_db")
        print("  DB_USER=root")
        print("  DB_PASSWORD=")
        return False

def check_dependencies():
    """Check file structure and dependencies"""
    print("\n" + "="*50)
    print("CHECKING FILE STRUCTURE")
    print("="*50)
    
    required_files = [
        'database/config.py',
        'database/schema.sql',
        'campaign/app.py',
        'requirements.txt'
    ]
    
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    all_exist = True
    for file in required_files:
        full_path = os.path.join(base_path, file)
        if os.path.exists(full_path):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} NOT found")
            all_exist = False
    
    return all_exist

def main():
    print("\n")
    print("#" * 50)
    print("# MYSQL SETUP VERIFICATION")
    print("#" * 50)
    
    checks = [
        ("Python Packages", check_python_packages),
        ("Environment Configuration", check_env_file),
        ("File Structure", check_dependencies),
        ("MySQL Connection", check_mysql_connection),
        ("Database Tables", check_database_tables),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error in {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*50)
    
    if all_passed:
        print("✓ All checks passed! Your setup is ready.")
        print("\nYou can now run: python campaign/app.py")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        print("\nFix the issues and run this script again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
