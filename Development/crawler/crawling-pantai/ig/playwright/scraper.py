from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()
usernm = os.getenv("usernm")
passwd = os.getenv("passwd")

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
    
    print("STEP 5: Navigating to homepage after login")
    page.goto("https://www.instagram.com/explore/tags/pantaisanur/")
    random_delay()

    print("STEP 6: Collecting post links")
    time.sleep(random.uniform(2, 4))
    post_links = page.locator('a[href^="/p/"]').all()
    unique_links = set()

    print(f"Found {len(post_links)} potential posts to process")
    for i, post in enumerate(post_links, 1):
        href = post.get_attribute("href")
        if href:
            full_url = f"https://www.instagram.com{href}"
            unique_links.add(full_url)
            print(f"  Processed {i}/{len(post_links)}: {full_url}")
        time.sleep(random.uniform(0.5, 1.5))

    print("\nFINAL RESULTS:")
    print(f"Found {len(unique_links)} unique posts:")
    for link in unique_links:
        print(link)
        time.sleep(0.2)

    print("\nScript completed successfully")
    time.sleep(random.uniform(2, 3))
    page.pause()
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)