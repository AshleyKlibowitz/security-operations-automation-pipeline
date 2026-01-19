import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USER = os.getenv('JIRA_USER')
JIRA_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

if not (JIRA_SERVER and JIRA_USER and JIRA_TOKEN and JIRA_PROJECT_KEY):
    print('Missing JIRA configuration in .env')
    raise SystemExit(1)

url = f"{JIRA_SERVER}/rest/api/2/issue"

payload = {
    "fields": {
        "project": {"key": JIRA_PROJECT_KEY},
        "summary": "Run python scanner.py",
        "description": "Automated task: please execute `python scanner.py` in the security project workspace.",
        "issuetype": {"name": "Task"}
    }
}

headers = {"Content-Type": "application/json", "Accept": "application/json"}

resp = requests.post(url, auth=(JIRA_USER, JIRA_TOKEN), headers=headers, data=json.dumps(payload))

if resp.status_code == 201:
    key = resp.json().get('key')
    print(f'[+] Jira issue created: {key} -- {JIRA_SERVER}/browse/{key}')
else:
    print(f'[-] Failed to create Jira issue: {resp.status_code}')
    try:
        print(resp.json())
    except Exception:
        print(resp.text)
