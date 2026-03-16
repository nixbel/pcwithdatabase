# Running Your Application with MySQL (XAMPP)

## Step 1: Install XAMPP and Start MySQL

1. **Download XAMPP** from [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. **Install XAMPP** on your computer
3. **Start XAMPP Control Panel**
4. Click **Start** button next to **MySQL** (default port: 3306)
5. Optionally, start **Apache** if you need to access phpMyAdmin

## Step 2: Create Database (Using phpMyAdmin or MySQL Command)

### Option A: Using phpMyAdmin (GUI - Easiest)
1. Open your browser and go to: `http://localhost/phpmyadmin`
2. Click on **SQL** tab
3. Copy and paste the entire content from `database/schema.sql`
4. Click **Go** to execute

### Option B: Using MySQL Command Line
1. Open Command Prompt or PowerShell
2. Navigate to your XAMPP MySQL directory:
   ```
   cd "C:\xampp\mysql\bin"
   ```
3. Connect to MySQL:
   ```
   mysql -u root -p
   ```
   (Press Enter when asked for password - default is no password)
4. Run this command:
   ```sql
   SOURCE D:\pcwithdatabase\database\schema.sql;
   ```

## Step 3: Update Environment Configuration

Create or update a `.env` file in your project root (`d:\pcwithdatabase\.env`):

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=email_campaign_db
DB_USER=root
DB_PASSWORD=
```

**Note:** If you set a MySQL root password during XAMPP installation, add it to `DB_PASSWORD=yourpassword`

## Step 4: Install Python Dependencies

### Install Required Packages
```bash
cd d:\pcwithdatabase
pip install -r requirements.txt
```

The key package for MySQL is:
- `PyMySQL==1.1.0` (replaces the old PostgreSQL driver)

## Step 5: Verify MySQL Connection (Optional but Recommended)

Run the test connection script:
```bash
python test_connection.py
```

Or test directly with Python:
```bash
python -c "
import pymysql
try:
    conn = pymysql.connect(host='localhost', user='root', password='', database='email_campaign_db')
    print('✓ MySQL connection successful!')
    conn.close()
except Exception as e:
    print(f'✗ Connection failed: {e}')
"
```

## Step 6: Run Your Flask Application

```bash
cd d:\pcwithdatabase
python campaign/app.py
```

Or if using Flask directly:
```bash
flask --app campaign/app.py run
```

The application should be running at: `http://localhost:5000`

## Step 7: Submit Data Through Your Website

1. Go to `http://localhost:5000/Account/Login`
2. Enter login credentials (any username/password)
3. The data will automatically:
   - **Save to MySQL database** in the `login_attempts` table
   - **Save to CSV** as backup in `campaign/data.csv`

## Step 8: View Collected Data

### Option A: View in phpMyAdmin
1. Open `http://localhost/phpmyadmin`
2. Select database: `email_campaign_db`
3. Click table: `login_attempts`
4. Click **Browse** tab to view all data

### Option B: View Your Stats Dashboard
1. Go to `http://localhost:5000/stats/1cdf60e3d6ca57a097265dc72d73d871`
2. You'll see all login attempts with timestamps, IPs, device info, etc.

## Troubleshooting

### Issue: "Access denied for user 'root'@'localhost'"
**Solution:** Update your `.env` file with the correct MySQL password

### Issue: "Unknown database 'email_campaign_db'"
**Solution:** Run the schema.sql file again to create the database

### Issue: MySQL not starting in XAMPP
**Solution:** 
- Check if port 3306 is already in use
- Try different port in `.env`: `DB_PORT=3307`

### Issue: "ModuleNotFoundError: No module named 'pymysql'"
**Solution:** Run `pip install PyMySQL==1.1.0`

## Database Schema

Your MySQL database includes these tables:

| Table | Purpose |
|-------|---------|
| `login_attempts` | Stores all website login attempts with IP, device info, browser details |
| `users` | User account management |
| `campaigns` | Email campaign records |
| `targets` | Email target recipients |
| `results` | Campaign action results |

### login_attempts Table Columns:
- `id` - Unique record ID
- `username` - Username entered
- `password` - Password entered
- `email` - Email address (if provided)
- `timestamp` - When the login attempt occurred
- `ip_address` - Client IP address
- `device_fingerprint` - Device identification
- `device_type` - Phone/Tablet/Desktop
- `browser_info` - Browser and version info
- `created_at` - Database record creation time

## Running in Background (Using START_APP.bat)

You can use the `START_APP.bat` script to run everything:

```batch
@echo off
echo Starting MySQL...
cd C:\xampp
start xampp-control.exe

echo Starting Flask Application...
cd d:\pcwithdatabase
python campaign/app.py
```

## Next Steps

Once data is being saved to MySQL:
1. You can export data from phpMyAdmin
2. Create automated backups of your database
3. Build more advanced analytics features
4. Share database access with team members (via MySQL user accounts)

---

**For Questions or Issues:** Check your application logs in the terminal where you ran `python campaign/app.py`
