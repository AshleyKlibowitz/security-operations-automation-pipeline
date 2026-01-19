import socket
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CONFIGURATION
TARGET_IP = '127.0.0.1'
TEST_PUBLIC_IP = '1.1.1.1' 
LOG_FILE = 'logs/scanner_logs.json'
SIMULATION_MODE = True 

# JIRA CONFIG
JIRA_USER = os.getenv('JIRA_USER')
JIRA_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

def create_jira_ticket(ip, port, risk_score):
    """
    Creates a Jira ticket for the detected vulnerability.
    """
    if not JIRA_USER or not JIRA_TOKEN:
        print("[-] Jira credentials missing. Skipping ticket creation.")
        return

    url = f"{JIRA_SERVER}/rest/api/2/issue"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"Security Alert: Port {port} Open on {ip}",
            "description": f"Automated Scan Report.\n\nTarget: {ip}\nPort: {port}\nStatus: OPEN\nAbuseIPDB Risk Score: {risk_score}\n\nPlease investigate immediately.",
            "issuetype": {
                "name": "Task" 
            }
        }
    })

    try:
        response = requests.post(url, headers=headers, data=payload, auth=(JIRA_USER, JIRA_TOKEN))
        
        if response.status_code == 201:
            print(f"[+] SUCCESS: Jira Ticket Created! (Key: {response.json()['key']})")
        else:
            print(f"[-] FAILED to create Jira ticket. Status: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[-] Error connecting to Jira: {e}")

def get_ip_reputation(ip_address):
    # (Same as before - keeping it brief)
    if not os.getenv('ABUSEIPDB_API_KEY'): return 0
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Key': os.getenv('ABUSEIPDB_API_KEY'), 'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, params={'ipAddress': ip_address})
        return response.json()['data']['abuseConfidenceScore']
    except: return 0

def scan():
    results = []
    print(f"--- Starting Scan on {TARGET_IP} ---")
    
    # 1. Get Risk Score
    risk_score = get_ip_reputation(TEST_PUBLIC_IP)

    # 2. Simulation Logic
    if SIMULATION_MODE:
        print("[*] SIMULATION MODE: Force-logging threat.")
        port = 8080
        
        # Log to file
        results.append({
            "timestamp": datetime.now().isoformat(),
            "ip": TARGET_IP,
            "port": port,
            "status": "OPEN",
            "risk_score": risk_score
        })
        
        # 3. TRIGGER WORKFLOW: Create Jira Ticket
        print("[*] Attempting to create Jira ticket...")
        create_jira_ticket(TARGET_IP, port, risk_score)

    # Write logs
    with open(LOG_FILE, 'w') as f:
        json.dump(results, f, indent=4)
    print("--- Scan Complete ---")

if __name__ == "__main__":
    scan()
import socket
import json
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# CONFIG
TARGET_IP = '127.0.0.1'
PORTS = [22, 80, 443, 8080]
TEST_PUBLIC_IP = '1.1.1.1'  # Public test IP for AbuseIPDB queries
LOG_FILE = 'logs/scanner_logs.json'
API_KEY = os.getenv('ABUSEIPDB_API_KEY')
SOCKET_TIMEOUT = 1.0


def ensure_log_file():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)


def append_log(entry):
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_ip_reputation(ip_address):
    """Query AbuseIPDB for an abuse confidence score for a public IP.

    If `ABUSEIPDB_API_KEY` is not set, returns 0 and prints a notice.
    """
    if not API_KEY:
        print("[i] ABUSEIPDB_API_KEY not set; skipping reputation lookup (returning 0).")
        return 0

    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Key': API_KEY, 'Accept': 'application/json'}
    params = {'ipAddress': ip_address}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        body = resp.json()
        score = body.get('data', {}).get('abuseConfidenceScore', 0)
        print(f"[i] AbuseIPDB {ip_address} risk score: {score}")
        return score
    except Exception as e:
        print(f"[!] AbuseIPDB lookup failed: {e}")
        return 0


def scan_ports():
    ensure_log_file()
    print(f"--- Starting Scan on {TARGET_IP} ---")
    logged = 0

    for port in PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(SOCKET_TIMEOUT)
        try:
            result = s.connect_ex((TARGET_IP, port))
            if result == 0:
                print(f"Port {port} is OPEN")
                # When we find an open port on localhost, enrich using the public test IP
                risk = get_ip_reputation(TEST_PUBLIC_IP)
                entry = {
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'ip': TARGET_IP,
                    'port': port,
                    'status': 'OPEN',
                    'risk_score': risk
                }
                append_log(entry)
                logged += 1
            else:
                print(f"[-] Port {port} is closed")
        finally:
            s.close()

    print(f"--- Scan Complete. Logged {logged} issues to {LOG_FILE} ---")


if __name__ == '__main__':
    scan_ports()