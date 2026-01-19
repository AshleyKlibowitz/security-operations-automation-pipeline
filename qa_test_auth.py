from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from .env
JIRA_PROJECT = os.getenv('JIRA_PROJECT_KEY', 'KAN')
BASE_URL = os.getenv('JIRA_SERVER')
TARGET_URL = f"{BASE_URL}/jira/software/projects/{JIRA_PROJECT}/boards/2"


def run_qa_auth():
    print("--- Starting Automated QA Test (auth.json) ---")
    if not os.path.exists('auth.json'):
        print('[-] auth.json not found. Run `setup_auth.py` first to save a storage state.')
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state='auth.json')
        page = context.new_page()

        print("[*] Navigating to Board using saved auth...")
        page.goto(TARGET_URL)

        try:
            page.wait_for_selector('text=KAN', timeout=20000)
            print('[+] SUCCESS: Project Board found (via auth.json)!')
            os.makedirs('logs', exist_ok=True)
            page.screenshot(path='logs/qa_success_auth.png')
            print('[+] Screenshot saved: logs/qa_success_auth.png')
        except Exception as e:
            print('[-] Automation failed to find the board:', e)
            os.makedirs('logs', exist_ok=True)
            page.screenshot(path='logs/qa_error_auth.png')
            print('[+] Screenshot saved: logs/qa_error_auth.png')

        browser.close()


if __name__ == '__main__':
    run_qa_auth()
