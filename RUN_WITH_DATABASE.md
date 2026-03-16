# How to Run Your Application with PostgreSQL Database

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Configuration](#configuration)
4. [Starting the Application](#starting-the-application)
5. [Inputting Data & Seeing Results](#inputting-data--seeing-results)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Make sure you have installed:
- Python 3.8+
- PostgreSQL 12+ (with pgAdmin4 optional)
- pip (Python package manager)

### Check Installation:
```bash
python --version
psql --version
```

---

## Database Setup

### Step 1: Create PostgreSQL Database

Open Command Prompt/PowerShell and connect to PostgreSQL:
```bash
psql -U postgres
```

Create the database:
```sql
CREATE DATABASE campaign_db_2mv9;
```

Exit psql:
```sql
\q
```

### Step 2: Initialize Database Tables

Run the initialization script from your workspace:
```bash
cd d:\pcwithdatabase
python -c "from database.init_db import init_db; init_db()"
python -c "from database.login_operations import create_login_attempts_table; create_login_attempts_table()"
```

Expected output:
```
INFO:root:Database connection pool initialized successfully
INFO:root:Login attempts table created successfully!
```

---

## Configuration

### Step 1: Update .env File

Edit `d:\pcwithdatabase\.env` and update with your local PostgreSQL credentials:

```
# Local Database Configuration
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=campaign_db_2mv9
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
```

Replace `your_actual_password_here` with your PostgreSQL password.

### Step 2: Verify Dependencies

Make sure all required packages are installed:
```bash
cd d:\pcwithdatabase
pip install -r requirements.txt
```

If any packages fail, install them individually:
```bash
pip install Flask psycopg2-binary python-dotenv
```

---

## Starting the Application

### Step 1: Start PostgreSQL
Make sure PostgreSQL is running:
```bash
# On Windows, PostgreSQL typically starts automatically
# If not, start it from Services or:
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
```

### Step 2: Run the Flask Application

```bash
cd d:\pcwithdatabase\campaign
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
 * WARNING in use_werkzeug_debugger: Debugger is active!
 * Press CTRL+C to quit
```

### Step 3: Access the Website

Open your web browser and go to:
```
http://localhost:5000
```

You should see the login page.

---

## Inputting Data & Seeing Results

### Method 1: Through the Website (Recommended)
1. Navigate to `http://localhost:5000`
2. Fill in the form with your data
3. Click Submit
4. Data is automatically saved to PostgreSQL database

### Method 2: View Data in Database

#### Using pgAdmin4:
1. Open pgAdmin4
2. Connect to your local PostgreSQL server
3. Navigate to: `Databases → campaign_db_2mv9 → Schemas → public → Tables`
4. Right-click on `login_attempts` → **View/Edit Data**
5. Click the "+" button to see all entered data

#### Using Command Line:
```bash
psql -U postgres -d campaign_db_2mv9 -c "SELECT * FROM login_attempts;"
```

#### Using Python Script (in workspace):
```bash
python -c "from database.login_operations import get_all_login_attempts; 
attempts = get_all_login_attempts(); 
import pprint; 
pprint.pprint(attempts)"
```

### Method 3: Verify Data Sync

The application saves data in two places:
1. **CSV File**: `campaign/data.csv` (for backup)
2. **PostgreSQL Database**: `login_attempts` table (primary storage)

Both are synchronized automatically.

---

## Complete Startup sequence

Here's the complete process to get everything running:

```bash
# 1. Navigate to project directory
cd d:\pcwithdatabase

# 2. Verify and update .env file
# Open in notepad and update DB credentials
notepad .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database tables
python -c "from database.init_db import init_db; init_db()"
python -c "from database.login_operations import create_login_attempts_table; create_login_attempts_table()"

# 5. Start Flask application
cd campaign
python app.py

# 6. Access the website
# Open http://localhost:5000 in your web browser
```

---

## Troubleshooting

### Issue: "psycopg2: FATAL: role 'postgres' does not exist"
**Solution**: 
```bash
psql -U postgres
```
If this fails, PostgreSQL may not be running. Check Services (Windows) and start PostgreSQL.

### Issue: "Connection refused" when trying to connect
**Solution**: 
```bash
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# If not running, start it
# Windows Services → PostgreSQL → Start
```

### Issue: "Database does not exist"
**Solution**: 
Create the database first:
```bash
psql -U postgres -c "CREATE DATABASE campaign_db_2mv9;"
```

### Issue: "ModuleNotFoundError: No module named 'database'"
**Solution**:
Make sure you're running from the correct directory with `__init__.py` files:
```bash
cd d:\pcwithdatabase
python campaign/app.py
```

### Issue: Data not showing in database
**Solution**:
1. Check if Flask is running without errors
2. Verify `.env` file has correct credentials
3. Check `campaign/data.csv` to see if data is at least saving to CSV
4. Run: `psql -U postgres -d campaign_db_2mv9 -c "SELECT * FROM login_attempts;"`

---

## What Happens When You Submit Form Data?

1. **User inputs data** on the website form
2. **Flask catches the POST request** in `campaign/app.py`
3. **Data is processed** and extracted
4. **Two-way save**:
   - Saved to `campaign/data.csv` as backup
   - Saved to PostgreSQL `login_attempts` table as primary storage
5. **User sees confirmation** (redirect or response)
6. **You can view results** in database using methods above

---

## Database Schema

### login_attempts Table:
```sql
CREATE TABLE login_attempts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    timestamp VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    device_fingerprint VARCHAR(255),
    device_type VARCHAR(50),
    browser_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

Columns explained:
- `id`: Unique identifier for each entry
- `username`: User's input username
- `password`: User's input password
- `timestamp`: When data was submitted
- `ip_address`: User's IP address
- `device_fingerprint`: Device identifier
- `device_type`: Desktop/Mobile/Tablet
- `browser_info`: Browser details (JSON format)
- `created_at`: Database timestamp

---

**Happy coding!** 🚀 If you need to check data frequently, consider using pgAdmin4 for a user-friendly interface.
