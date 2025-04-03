import csv
import requests
import re
import time
from bs4 import BeautifulSoup

def write_to_csv(data, filename):
    file_empty = False
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if not f.read():
                file_empty = True
    except FileNotFoundError:
        file_empty = True

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file_empty:
            writer.writerow(['title', 'link', 'date', 'content', 'is_fake'])
        for row in data:
            writer.writerow(row)

# Untuk membuat string tanggal sesuai dengan dalam website
def get_date():
    bulan = {
        "January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
        "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
        "September": "September", "October": "Oktober", "November": "November", "December": "Desember"
    }

    raw_date = get_raw_date()
    for eng, indo in bulan.items():
        raw_date = raw_date.replace(eng, indo)
    return raw_date

# Tanggal yang dimasukkan ke csv. 
def get_raw_date():
    return time.strftime("%d %B %Y", time.localtime())

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

# Jika judul = "hoaks!" atau "disinformasi!", maka judul, link, tanggal, dan konten akan diambil.
def find_hoax(links_dict):
    data = []
    raw_date = get_raw_date()
    for title, link in links_dict.items():
        if "hoaks!" in title.lower() or "disinformasi!" in title.lower():
            try:
                get_content = requests.get(link, timeout=10)
                get_content.raise_for_status()
                date = raw_date
                content = find_content(link)
                is_fake = 1
                data.append([title, link, date, content, is_fake])
            except requests.exceptions.RequestException as e:
                print(f"Error fetching content for {link}: {e}")
        time.sleep(2)
    return data

# Mencari konten dari link berita.
def find_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

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
        return " ".join(paragraphs)
    return ""

def tocsv(data):
    filename = 'dataset_antara_hoaks_raw.csv'
    write_to_csv(data, filename)
    print(f"Data has been written to {filename}")

def clean_csv():
    with open('dataset_antara_hoaks_raw.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        modified_data = []
        for row in reader:
            title, link, date, content, is_fake = row
            extracted_content = extract_content(content)
            modified_data.append([title, link, date, extracted_content, is_fake])

    filename = 'dataset_antara_hoaks.csv'
    write_to_csv(modified_data, filename)
    print(f"Data has been written to {filename}")

def extract_content(text):
    text = text.lower()
    start_phrases = ["jakarta (antara) - "]
    start_pattern = "|".join(map(re.escape, start_phrases))
    pattern = f"({start_pattern})(.*)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(2).strip() if match else text

def main():
    url = 'https://www.antaranews.com/tag/cek-fakta/'
    links_dict = find_links(url)
    data = find_hoax(links_dict)
    tocsv(data)
    clean_csv()

if __name__ == "__main__":
    main()
