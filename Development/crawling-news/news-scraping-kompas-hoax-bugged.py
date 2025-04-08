import csv
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Function to write data to CSV file
def write_to_csv(data, filename, write_header=False):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if write_header:
            # Write header row
            writer.writerow(['title', 'link', 'date', 'content', 'is_fake'])
        # Write data rows
        for row in data:
            writer.writerow(row)
    

# Ambil tanggal hari ini, untuk masukkan ke CSV
def get_date():
   return datetime.today().strftime('%d/%m/%Y')

# URL untuk halaman-halaman berikutnya, kalo page 1 pakai url biasa. 
def get_url(base_url, page):
   return f"{base_url}/{page}" if page > 1 else base_url
  
def extract_content(text):
    text = text.lower()

    # Kata-kata yang biasanya ada di awal berita
    start_phrases = [
        "kompas.com - ",
        ".kompas.com",
        "kompas.com-"]

    start_pattern = "|".join(map(re.escape, start_phrases))
    pattern = f"({start_pattern})(.*)"

    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(2).strip()
    else:
        return text
    
# Fungsi utama buat ambil data dari web Kompas hoaks atau fakta
def get_data():
    # Ambil tanggal hari ini buat filter berita
    today = datetime.today().strftime('%d/%m/%Y')
    data = []
    url = get_url('https://www.kompas.com/cekfakta/hoaks-atau-fakta', 1)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    news_items = soup.find_all('a', class_='cekfakta-list-link')
    for item in news_items:
        # Cek tanggal berita
        date_elem = item.find('p', class_='cekfakta-text-date')

        date_str = date_elem.get_text(strip=True).split(',')[0]
        if date_str != today:
            break  # Stop if we find an older date
        
        title = item.find('h1').get_text(strip=True)
        part_title = title.split(']')

        category = "UNKNOWN"  

        if len(part_title) == 2:
            category = part_title[0].strip('[').strip()
            title = part_title[1].strip()
        
        link = item['href']

        content_response = requests.get(link)
        content_soup = BeautifulSoup(content_response.text, 'html.parser')
        content_paragraphs = content_soup.find('div', class_='read__content').find_all('p')
        content = ' '.join(p.get_text(strip=True) for p in content_paragraphs)
        extracted_content = extract_content(content)

        is_fake = 1 if category != "HOAKS" else 0  

        data.append([title, link, today, extracted_content, is_fake])
    return data

def modify_csv(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        next(reader)

        modified_data = []

        for row in reader:
            title = row[0]
            link = row[1]
            date = row[2]
            content = row[3]
            is_fake = row[4]

            extracted_content = extract_content(content)

            modified_data.append([title, link, date, extracted_content, is_fake])

        filename = 'dataset_kompas_hoaks.csv'

        write_to_csv(modified_data, filename, write_header=True)

        print(f"Data has been written to {filename}")

def main():
    data = get_data()
    filename = 'dataset_raw_kompas_hoaks.csv'
    write_to_csv(data, filename, write_header=True)
    modify_csv(filename)

if __name__ == '__main__':
    main()