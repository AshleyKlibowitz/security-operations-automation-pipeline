from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

# CONFIGURATION: build board URL from .env
# Override by setting `JIRA_SERVER` in your local `.env` file.
JIRA_SERVER = os.getenv('JIRA_SERVER', 'https://your-domain.atlassian.net')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'KAN')
# You may need to update board id if different
JIRA_BOARD_URL = f"{JIRA_SERVER}/jira/software/projects/{JIRA_PROJECT_KEY}/boards/35"

def save_auth():
    print("--- Manual Login Helper ---")
    print("[*] I will open a browser. Please log in with Google manually.")
    print("[*] Once you see your Jira Board, close the browser window.")

    with sync_playwright() as p:
        # Launch browser (not headless, so you can see it)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Go to Jira
        page.goto(JIRA_BOARD_URL)

        # We wait until the specific "Board" element loads, confirming you are in.
        try:
            # Wait up to 3 minutes for you to finish Google login
            print("--- WAITING FOR YOU TO LOG IN... ---")
            page.wait_for_selector('text=Security Alert', timeout=180000)
            print("[+] Login detected! Saving cookies...")
            
            # Save the cookies to a file
            context.storage_state(path="auth.json")
            print("[+] SUCCESS: Session saved to 'auth.json'.")
            
        except Exception as e:
            print("[-] Timed out or closed too early. Did you log in?")

        browser.close()

if __name__ == "__main__":
    save_auth()
