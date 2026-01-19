from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_PROJECT = os.getenv('JIRA_PROJECT_KEY', 'KAN')
BASE_URL = os.getenv('JIRA_SERVER')
TARGET_URL = f"{BASE_URL}/jira/software/projects/{JIRA_PROJECT}/boards/2"

OUTPUT_PATH = 'logs/qa_third.png'


def run():
    print('--- Starting QA Screenshot Helper ---')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"[*] Navigating to {TARGET_URL} ...")
        try:
            page.goto(TARGET_URL, timeout=60000)
        except Exception as e:
            print('[!] Navigation warning:', e)

        print('[*] Waiting for board to render (up to 120s). Please complete any interactive login in the opened browser.')
        try:
            page.wait_for_selector('text=KAN', timeout=120000)
            print('[+] Board detected — saving screenshot.')
            os.makedirs('logs', exist_ok=True)
            page.screenshot(path=OUTPUT_PATH)
            print(f'[+] Screenshot saved: {OUTPUT_PATH}')
        except Exception as e:
            print('[!] Timeout or error waiting for board:', e)
            os.makedirs('logs', exist_ok=True)
            page.screenshot(path=OUTPUT_PATH.replace('.png', '_error.png'))
            print(f'[+] Error screenshot saved: {OUTPUT_PATH.replace('.png', '_error.png')}')

        browser.close()


if __name__ == '__main__':
    run()
