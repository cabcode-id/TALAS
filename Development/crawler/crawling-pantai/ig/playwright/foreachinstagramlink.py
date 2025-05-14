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

def process_instagram_post(page, link):
    print(f"Processing post: {link}")
    data = {
        'source': 'Instagram',
        'date': 'N/A',
        'content': 'N/A',
        'comments': [],
        'image': 'N/A',
        'link': link
    }
    
    try:
        page.goto(link)
        random_delay()

        date_element = page.locator('time').filter(has_text="2025").first
        if date_element:
            data['date'] = date_element.get_attribute('datetime')
            print(f"Found date: {data['date']}")

        # Extract content - modified version to get all text from h1 tag
        content_element = page.locator('h1').first
        if content_element:
            # Get all text content including line breaks and hashtags
            data['content'] = content_element.inner_text()
            print(f"Found content: {data['content']}")
        else:
            print("Warning: No h1 content found")   

        # Extract comments (up to 10)
        comment_elements = page.locator('ul._a9ym li._a9zj._a9zl').all()
        for comment in comment_elements[:10]:
            comment_text_element = comment.locator('div.xt0psk2 span._ap3a').first
            if comment_text_element:
                data['comments'].append(comment_text_element.inner_text())

        # Extract image URL
        image_element = page.locator('div._aagv img').first
        if image_element:
            data['image'] = image_element.get_attribute('src')

        print(f"Successfully processed: {link}")
    except Exception as e:
        print(f"Error processing {link}: {str(e)}")
    
    return data

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Direct Instagram link to process
    link = "https://www.instagram.com/p/DB3XAEdTrg6/"  # Replace with your actual Instagram post URL
    
    # Login to Instagram first
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

    # Process the Instagram post
    post_data = process_instagram_post(page, link)

    # Print the extracted data
    print("\nExtracted Post Data:")
    print(f"Source: {post_data['source']}")
    print(f"Date: {post_data['date']}")
    print(f"Content: {post_data['content']}")
    print(f"Image URL: {post_data['image']}")
    print(f"Link: {post_data['link']}")
    print("Comments:")
    for i, comment in enumerate(post_data['comments'], 1):
        print(f"{i}. {comment}")

    # Write data to CSV
    csv_filename = f"instagram_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'date', 'content', 'comments', 'image', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Convert comments list to semicolon-separated string
        row = post_data.copy()
        row['comments'] = '; '.join(row['comments'])
        writer.writerow(row)
    
    print(f"\nData saved to {csv_filename}")

    # Close browser
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)