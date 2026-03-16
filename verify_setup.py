"""
Setup Verification Script
Checks if all components are properly configured before running the application
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_mark():
    return "✓"

def x_mark():
    return "✗"

def check_python():
    """Verify Python is installed"""
    print(f"\n{check_mark()} Python {sys.version.split()[0]} is installed")
    return True

def check_dotenv():
    """Verify .env file exists and has correct variables"""
    env_path = Path(".env")
    if not env_path.exists():
        print(f"{x_mark()} .env file not found")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing.append(var)
        
        if missing:
            print(f"{x_mark()} Missing environment variables: {', '.join(missing)}")
            print(f"   Please update .env file")
            return False
        
        print(f"{check_mark()} .env file found and configured correctly")
        print(f"   Database: {os.getenv('DB_NAME')} on {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
        return True
    except Exception as e:
        print(f"{x_mark()} Error reading .env file: {e}")
        return False

def check_packages():
    """Verify required packages are installed"""
    required_packages = [
        'flask',
        'psycopg2',
        'python_dotenv',
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{x_mark()} Missing packages: {', '.join(missing_packages)}")
        print(f"   Run: pip install -r requirements.txt")
        return False
    
    print(f"{check_mark()} All required packages are installed")
    return True

def check_database_modules():
    """Verify database modules exist"""
    required_files = [
        'database/__init__.py',
        'database/config.py',
        'database/connection.py',
        'database/init_db.py',
        'database/login_operations.py',
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"{x_mark()} Missing database modules: {', '.join(missing_files)}")
        return False
    
    print(f"{check_mark()} All database modules are present")
    return True

def check_flask_app():
    """Verify Flask app structure"""
    required_files = [
        'campaign/app.py',
        'campaign/templates/index.html',
        'campaign/static/css/styles.css',
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"{x_mark()} Missing Flask files: {', '.join(missing_files)}")
        return False
    
    print(f"{check_mark()} Flask application structure is complete")
    return True

def check_database_connection():
    """Test database connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        import psycopg2
        
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        print(f"{check_mark()} Database connection successful!")
        return True
    
    except psycopg2.OperationalError as e:
        print(f"{x_mark()} Cannot connect to database")
        print(f"   Error: {str(e)}")
        print(f"   Make sure PostgreSQL is running and .env credentials are correct")
        return False
    except Exception as e:
        print(f"{x_mark()} Database connection error: {str(e)}")
        return False

def main():
    print_header("SETUP VERIFICATION SCRIPT")
    print("\nThis script will verify that your application is properly configured.")
    print("Running checks...\n")
    
    checks = [
        ("Python Installation", check_python),
        ("Environment File (.env)", check_dotenv),
        ("Required Packages", check_packages),
        ("Database Modules", check_database_modules),
        ("Flask Application", check_flask_app),
        ("Database Connection", check_database_connection),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"{x_mark()} {name}: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = check_mark() if result else x_mark()
        print(f"{status} {name}")
    
    print()
    
    if all_passed:
        print("✓ All checks passed! Your application is ready to run.")
        print("\nYou can now start the application:")
        print("  Option 1: Run START_APP.bat (Windows)")
        print("  Option 2: Run 'python campaign/app.py' manually")
        print("  Option 3: Run: python START_APP.bat")
        print("\nThen access http://localhost:5000 in your web browser.")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above before running the app.")
        print("\nFor help, check RUN_WITH_DATABASE.md for detailed instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
