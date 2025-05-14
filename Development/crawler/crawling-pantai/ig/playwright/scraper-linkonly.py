from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os
import time
import random
import json

# Load environment variables
load_dotenv()
usernm = os.getenv("usernm")
passwd = os.getenv("passwd")

# Random delay parameters (in seconds)
MIN_DELAY = 5
MAX_DELAY = 10

def random_delay():
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

def scroll_page(page):
    # Scroll 3-5 times
    scroll_times = 10
    print(f"Scrolling page {scroll_times} times...")
    
    for i in range(scroll_times):
        # Scroll down
        page.mouse.wheel(0, 1500)
        # Random mouse movement
        page.mouse.move(random.randint(0, 500), random.randint(0, 500))
        # Wait for content to load
        time.sleep(random.uniform(2, 4))

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print("STEP 1: Navigating to Instagram homepage")
    page.goto("https://www.instagram.com/")
    random_delay()
    
    print("STEP 2: Filling username")
    page.get_by_label("Phone number, username, or email").click()
    random_delay()
    page.get_by_label("Phone number, username, or email").fill(usernm)
    random_delay()
    
    print("STEP 3: Filling password")
    page.get_by_label("Password").click()
    random_delay()
    page.get_by_label("Password").fill(passwd)
    random_delay()
    
    print("STEP 4: Clicking login button")
    page.get_by_role("button", name="Log in", exact=True).click()
    page.wait_for_url("https://www.instagram.com/accounts/onetap/?next=%2F")
    random_delay()

    # Navigate to the hashtag page
    page.goto("https://www.instagram.com/explore/tags/pantaisanur/")
    random_delay()

    # Scroll the page multiple times before collecting links
    scroll_page(page)

    # Collect post links
    anchors = page.locator('a[href^="/p/"]')
    time.sleep(random.uniform(2, 4))  # allow content to load
    hrefs = anchors.evaluate_all("els => els.map(el => el.href)")
    unique_links = sorted(set(hrefs))

    # Save links to JSON file
    data = {"links": unique_links}
    with open("scraper.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Collected {len(unique_links)} unique links. Saved to scraper.json")

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)
