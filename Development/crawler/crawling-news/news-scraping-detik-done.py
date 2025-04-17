import datetime
import requests
from bs4 import BeautifulSoup
import os
import csv
import time 
import re
from scraper_config import get_output_path

# Tanggal yang mau dimasukkan ke csv
def current_date():
    return datetime.date.today().strftime("%Y-%m-%d")

# URL yang mau discrape
def generate_url():
    today = datetime.date.today()
    formatted_date = today.strftime("%m%%2F%d%%2F%Y")  # MM%2FDD%2FYYYY
    return f"https://news.detik.com/berita/indeks?date={formatted_date}"

# Buat list halaman-halaman yang ada pada tanggal tsb (page 1, page 2, page 3, etc.)
def get_numbered_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Cari prev dan next
    prev_next_link = soup.find('a', string=lambda text: text and text.strip().lower() in ["prev", "next"])

    if prev_next_link:
        parent = prev_next_link.find_parent()  # Cari parent dari prev/next
        if parent:
            numbered_links = set() 
            for anchor in parent.find_all('a', href=True):
                text = anchor.text.strip()
                if text.isdigit() and 1 <= int(text) <= 9: # Hanya ambil page 1-9
                    if text.lower() not in ["prev", "next"]:  # Exclude prev and next
                        numbered_links.add(anchor['href'])
            return list(numbered_links)
    return []

# Ambil artikel dari halaman tsb
def get_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = {}  

    # Cari h3 yang berisi judul artikel
    for h3 in soup.find_all('h3', class_='media__title'):
        a_tag = h3.find('a', class_='media__link', href=True)
        if a_tag:
            title = a_tag.get_text(strip=True) 
            link = a_tag['href']

           
            if link not in articles:
                articles[link] = title

    return articles

def extract_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari div yang berisi konten artikel
        content_div = soup.find('div', class_='detail__body-text')
        if content_div:
            paragraphs = content_div.find_all('p')
            paragraph_text = ' '.join(p.get_text(strip=True) for p in paragraphs)  # Join text without newlines
            return paragraph_text
        return "" 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

def write_to_csv(data, filename):
    output_path = get_output_path(filename)
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'source', 'url', 'image', 'date', 'content'])
        id_counter = 1
        for row in data:
            writer.writerow([id_counter, row[0], "Detik", row[1], "", row[2], row[3]])
            id_counter += 1

def extract_title(text):
    if not isinstance(text, str):
        text = str(text)
    
    text = text.lower()

    start_phrases = [
        "\n"
    ]

    start_pattern = "|".join(map(re.escape, start_phrases))
    pattern = f"({start_pattern})(.*)"

    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(2).strip()
    else:
        return text

def main():
    url = generate_url()
    pagination_links = get_numbered_links(url)
    articles = {}

    for page_link in pagination_links:
        page_articles = get_articles(page_link)
        if page_articles:
            for key, value in page_articles.items():
                if key in articles:
                    articles[key].extend(value if isinstance(value, list) else [value])
                else:
                    articles[key] = value if isinstance(value, list) else [value]   
    
    processed_data = []
    for link, title in articles.items():
        raw_content = extract_content(link)
        date = current_date()
        processed_title = extract_title(title)
        processed_data.append([processed_title, link, date, raw_content])
        time.sleep(2)  

    filename = 'dataset_detik.csv'
    write_to_csv(processed_data, filename)
    print(f"Data has been written to {get_output_path(filename)}")

if __name__ == "__main__":
    main()


