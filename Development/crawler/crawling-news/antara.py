import csv
import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Tanggal yang dimasukkan ke csv. 
def get_raw_date():
    return datetime.today().strftime("%Y-%m-%d")

# Membuat dictionary berisi judul dan link yang dibuat beberapa jam lalu atau kemarin. 
def find_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find_all('div', class_='col-md-8')

    span_elements = []

    for div in divs:
        spans = div.find_all('span', string=re.compile(r'jam|kemarin', re.IGNORECASE))
        span_elements.extend(spans)

    links_dict = {}
    for span in span_elements:
        parent = span.find_parent()
        while parent:
            link = parent.find('a', href=True)
            if link:
                title = link.get('title', '')
                links_dict[title] = link['href']
                break
            parent = parent.find_parent()
    return links_dict

# Mengumpulkan artikel dari link yang ditemukan.
def collect_articles(links_dict):
    data = []
    raw_date = get_raw_date()
    source = "antara"
    for title, link in links_dict.items():
        try:
            get_content = requests.get(link, timeout=10)
            get_content.raise_for_status()
            date = raw_date
            content, image_url = find_content(link)
            # Process content directly
            processed_content = extract_content(content)
            data.append([title, source, link, image_url, date, processed_content])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content for {link}: {e}")
        time.sleep(2)
    return data

# Mencari konten dari link berita.
def find_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract image URL
    image_url = ""
    image_div = soup.find('div', class_='wrap__article-detail-image')
    if image_div:
        img_tag = image_div.find('img', class_='img-fluid')
        if img_tag and img_tag.has_attr('src'):
            image_url = img_tag['src']
    
    parent_p_count = {}
    # Mencari semua parent yang memiliki p. Jumlah p yang tertinggi = main content yang ingin diambil.
    for p in soup.find_all('p'):
        # Skip paragraphs that have any class attribute
        if p.has_attr('class'):
            continue
        # Skip paragraphs that contain a span with class 'baca-juga'
        if p.find('span', class_='baca-juga'):
            continue

        parent = p.find_parent()
        if parent:
            parent_p_count[parent] = parent_p_count.get(parent, 0) + 1

    content_text = ""
    if parent_p_count:
        max_parent = max(parent_p_count, key=parent_p_count.get)
        paragraphs = []
        for p in max_parent.find_all('p'):
            if p.has_attr('class'):
                continue
            if p.find('span', class_='baca-juga'):
                continue
            text = p.get_text(" ", strip=True)
            paragraphs.append(text)
        content_text = " ".join(paragraphs)
    
    return content_text, image_url

def extract_content(text):
    text = text.lower()
    start_phrases = ["jakarta (antara) - "]
    start_pattern = "|".join(map(re.escape, start_phrases))
    pattern = f"({start_pattern})(.*)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(2).strip() if match else text

def crawl_antara():
    url = 'https://www.antaranews.com/tag/cek-fakta/'
    links_dict = find_links(url)
    data = collect_articles(links_dict)
    
    # Format data for return
    formatted_data = []
    for row in data:
        formatted_data.append({
            'title': row[0],
            'source': row[1],
            'url': row[2],
            'image': row[3],
            'date': row[4],
            'content': row[5]
        })
    
    return formatted_data

def main():
    return crawl_antara()

if __name__ == "__main__":
    main()
