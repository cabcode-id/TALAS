from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os
import time
import random
import json

# Load environment variables (if needed for authentication)
load_dotenv()

# Random delay parameters (in seconds)
MIN_DELAY = 1
MAX_DELAY = 3

def random_delay():
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to Google
    print("Navigating to Google...")
    page.goto("https://www.google.com")
    random_delay()

    # Perform search
    search_query = (
        'site:instagram.com intitle:"pantai sanur" after:2025-05-01 before:2025-05-15 '
        '-inurl:reel -inurl:tv -inurl:stories'
    )
    print("Entering search query...")
    search_box = page.locator('textarea.gLFyf')
    search_box.fill(search_query)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle")
    random_delay()

    # Ensure Web results filter
    try:
        page.get_by_text("Web", exact=True).first.click(timeout=10000)
    except:
        page.get_by_text("Lainnya", exact=True).first.click()
        page.wait_for_load_state("networkidle")
        page.get_by_text("Web", exact=True).first.click()
    page.wait_for_load_state("networkidle")
    random_delay()

    # Collect all Instagram links
    all_links = []
    page_number = 1

    while True:
        print(f"Processing page {page_number}...")
        results = page.locator('div.MjjYud')
        for result in results.all():
            link = result.locator('a[href*="instagram.com"]').first
            if link:
                href = link.get_attribute("href")
                if href and "instagram.com" in href:
                    all_links.append(href)
                    print(f"Found link: {href}")

        next_button = page.locator('#pnnext').first
        if not next_button.is_visible():
            break

        next_button.click()
        page.wait_for_load_state("networkidle")
        random_delay()
        page_number += 1

    # Output links as JSON
    print(json.dumps({"links": all_links}, indent=2))

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)