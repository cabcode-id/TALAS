from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv
import os
import time
import random
import csv
from datetime import datetime

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
    
    # Navigate to Google
    print("Navigating to Google...")
    page.goto("https://www.google.com")
    random_delay()

    # Perform search
    print("Entering search query...")
    search_query = 'site:instagram.com intitle:"pantai sanur" after:2025-05-12 before:2025-05-15 -inurl:reel -inurl:tv -inurl:stories'
    search_box = page.locator('textarea.gLFyf')
    search_box.fill(search_query)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle")
    random_delay()

    try:
        print("Attempting to click Web filter directly...")
        page.get_by_text("Web", exact=True).first.click(timeout=10000)
        print("Successfully clicked Web filter directly")
        page.wait_for_load_state("networkidle")
        random_delay()
    except Exception as e:
        print("Web filter not found directly, trying via More menu...")
        more_button = page.get_by_text("Lainnya", exact=True).first
        more_button.click()
        page.wait_for_load_state("networkidle")
        random_delay()
        
        try:
            print("Attempting to click Web filter via More menu...")
            page.get_by_text("Web", exact=True).first.click(timeout=10000)
            print("Successfully clicked Web filter via More menu")
            page.wait_for_load_state("networkidle")
            random_delay()
        except Exception as e:
            print("Failed to click Web filter even after expanding More menu")
            raise Exception("Could not find Web filter after multiple attempts")

    all_links = []
    page_number = 1

    while True:
        print(f"Processing page {page_number}...")
        
        # Extract Instagram links
        results = page.locator('div.MjjYud')
        for result in results.all():
            link = result.locator('a[href*="instagram.com"]').first
            if link:
                href = link.get_attribute("href")
                if href and "instagram.com" in href:
                    all_links.append(href)
                    print(f"Found link: {href}")

        # Check for next page
        next_button = page.locator('#pnnext').first
        if not next_button.is_visible():
            print("No more pages found")
            break

        print("Clicking next page...")
        next_button.click()
        page.wait_for_load_state("networkidle")
        random_delay()
        page_number += 1

    print("\nFinal Results:")
    print(f"Found {len(all_links)} Instagram links")

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

    # Process each Instagram post
    data_rows = []
    for link in all_links:
        print(f"Processing post: {link}")
        try:
            page.goto(link)
            page.wait_for_load_state("networkidle")
            random_delay()

            # Extract date
            date_element = page.locator('time._a9ze._a9zf').first
            date = date_element.get_attribute('datetime') if date_element else 'N/A'

            # Extract content
            content_element = page.locator('div._a9zr h1._ap3a').first
            content = content_element.inner_text() if content_element else 'N/A'

            # Extract comments (up to 10)
            comments = []
            comment_elements = page.locator('ul._a9ym li._a9zj._a9zl').all()
            for comment in comment_elements[:10]:
                comment_text_element = comment.locator('div.xt0psk2 span._ap3a').first
                if comment_text_element:
                    comments.append(comment_text_element.inner_text())

            # Extract image URL
            image_element = page.locator('div._aagv img').first
            image_url = image_element.get_attribute('src') if image_element else 'N/A'

            data_rows.append({  
                'source': 'Instagram',
                'date': date,
                'content': content,
                'comments': comments,
                'image': image_url
            })
            print(f"Successfully processed: {link}")
        except Exception as e:
            print(f"Error processing {link}: {str(e)}")
            continue

    # Write data to CSV
    csv_filename = f"instagram_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'date', 'content', 'comments', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data_rows:
            # Convert comments list to semicolon-separated string
            row['comments'] = '; '.join(row['comments'])
            writer.writerow(row)
    
    print(f"Data saved to {csv_filename}")

    # Close browser
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)