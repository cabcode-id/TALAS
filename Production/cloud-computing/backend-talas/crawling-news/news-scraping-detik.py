import csv
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Function to write data to CSV file
def write_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header row if file doesn't exist
        if not file_exists:
            writer.writerow(['title', 'link', 'date', 'content', 'is_fake'])
        # Write data rows
        for row in data:
            writer.writerow(row)

# URL and page count for crawling
url = 'https://news.detik.com/berita/indeks/'
END_PAGE = 5

# Initialize list to store data
data = []

# Crawling each page
for i in range(1, END_PAGE):
    url_page = f"{url}{i}"
    page = requests.get(url_page)
    if not page.ok:
        print(f"Failed to retrieve page {url_page}")
        continue

    soup = BeautifulSoup(page.text, 'html.parser')

    # Find all news articles
    news = soup.find_all('article', 'list-content__item')

    for n in news:
        title = n.find('h3', 'media__title').get_text()
        link = n.find('a', 'media__link')['href']
        timestamp = n.find('div', 'media__date').find('span')['d-time']
        timestamp_int = int(timestamp)
        date = datetime.fromtimestamp(timestamp_int).strftime('%d/%m/%Y')

        if link:
            # Get news content
            get_content = requests.get(link)
            if not get_content.ok:
                print(f"Failed to retrieve content from {link}")
                continue

            soup_content = BeautifulSoup(get_content.text, 'html.parser')
            content = soup_content.find('div', 'detail__body-text').find_all('p')
            paragraph = ' '.join(p.get_text() for p in content)

            # News information
            is_fake = 0

            # Append data to list
            data.append([title, link, date, paragraph, is_fake])

# File name for the raw CSV
filename = 'dataset_detik_raw.csv'

# Write crawled data to CSV file
write_to_csv(data, filename)

print(f"Data has been written to {filename}")

# Function to extract title text
def extract_title(text):
    # Normalize text to lowercase
    text = text.lower()

    # Define start phrases to find the actual title content
    start_phrases = [
        "\n"
    ]

    # Initialize the pattern with the start phrases
    start_pattern = "|".join(map(re.escape, start_phrases))
    pattern = f"({start_pattern})(.*)"

    # Use regular expressions to find content after the start phrases
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(2).strip()
    else:
        return text

# Open the CSV file in read mode to process titles
with open('dataset_detik_raw.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    # Skip the header row
    next(reader)

    # Create a list to store modified data
    modified_data = []

    # Iterate over each row in the CSV file
    for row in reader:
        title = row[0]
        link = row[1]
        date = row[2]
        content = row[3]
        is_fake = row[4]

        # Extract and normalize title
        extracted_title = extract_title(title)

        # Append modified data to the list
        modified_data.append([extracted_title, link, date, content, is_fake])

# File name for the final CSV
filename = 'dataset_detik.csv'

# Write modified data to CSV file
write_to_csv(modified_data, filename)

print(f"Data has been written to {filename}")
