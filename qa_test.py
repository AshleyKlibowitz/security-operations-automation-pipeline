from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_USER = os.getenv('JIRA_USER')
# Build the board URL from environment variables so this file is safe to commit.
# Set `JIRA_SERVER` and `JIRA_PROJECT_KEY` in your local `.env` (do not commit secrets).
JIRA_SERVER = os.getenv('JIRA_SERVER', 'https://your-domain.atlassian.net')
JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', 'KAN')
JIRA_BOARD_URL = f"{JIRA_SERVER}/jira/software/projects/{JIRA_PROJECT_KEY}/boards/2"

def run():
    print("--- Starting Final Automated QA Test ---")
    password = input(f"Enter Jira Password for {JIRA_USER}: ")

    with sync_playwright() as p:
        # slow_mo gives the Atlassian login cookies time to settle
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        page = browser.new_page()

        print("[*] Navigating to Atlassian ID...")
        page.goto("https://id.atlassian.com/login")

        # Step 1: Login
        page.fill('input[name="username"]', JIRA_USER)
        page.click('#login-submit')
        
        page.wait_for_selector('input[name="password"]')
        page.fill('input[name="password"]', password)
        page.click('#login-submit')

        # Step 2: The Direct Jump 
        # As soon as the login button is clicked, we force the browser 
        # to go to the Board, ignoring the 'Home' screen entirely.
        print("[*] Authentication complete. Jumping directly to the KAN Board...")
        
        # We wait for the URL to change away from the login page before jumping
        page.wait_for_url("**/home.atlassian.com/**", timeout=30000)
        page.goto(JIRA_BOARD_URL)

        # Step 3: Verification
        try:
            # We wait for the Project Key 'KAN' to appear on the cards
            print("[*] Waiting for board content to render...")
            page.wait_for_selector('text=KAN', timeout=30000)
            
            print("[+] SUCCESS: The robot has reached the Board!")
            
            if not os.path.exists('logs'): os.makedirs('logs')
            page.screenshot(path="logs/qa_success.png")
            print("[+] Final proof saved to logs/qa_success.png")
            
        except Exception as e:
            print(f"[-] Board verification failed: {e}")
            page.screenshot(path="logs/qa_stuck_state.png")
            print("[*] Check logs/qa_stuck_state.png to see what the robot saw.")

        browser.close()

if __name__ == "__main__":
    run()