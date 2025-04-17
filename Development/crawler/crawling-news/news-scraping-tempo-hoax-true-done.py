import csv
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from scraper_config import get_output_path

def get_date():
    return datetime.today().strftime("%Y-%m-%d")

def get_tempo_links():
    url = f'https://cekfakta.tempo.co/{datetime.now().strftime("%Y/%m")}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links_data = []
    
    for article in soup.find_all('article', class_='text-card'):
        date_text = article.find('h4', class_='date')
        if date_text and 'jam' in date_text.get_text():
            a_tag = article.find('a', href=True)
            if a_tag:
                link = "https:" + a_tag['href'] if a_tag['href'].startswith("//") else a_tag['href']
                links_data.append((a_tag.get_text().strip(), link))
    
    return list(set(links_data))

def extract_content(text):
    match = re.search(r"(jakarta -|jakarta-)(.*)", text.lower(), re.DOTALL)
    return match.group(2).strip() if match else text

def scrape_tempo_articles(tempo_links):
    data = []
    date = get_date()
    source = "Tempo"
    id_counter = 1
    
    for title, link in tempo_links:
        category, title_news = title.split(':', 1) if ':' in title else (title, title)
        is_fake = 1 if category in ["Menyesatkan", "Keliru"] else 0
        
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        detail_in = soup.find('div', 'detail-in')
        
        if detail_in:
            p = detail_in.find_all('p')
            content = ' '.join(p.get_text() for p in p)
            
            # Process content directly instead of writing to raw file first
            processed_content = extract_content(content)
            
            # Empty string for image
            image = ""
            
            data.append([id_counter, title_news, source, link, image, date, processed_content])
            id_counter += 1
    
    return data

def write_to_csv(data, filename):
    output_path = get_output_path(filename)
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'source', 'url', 'image', 'date', 'content'])
        writer.writerows(data)

def main():
    tempo_links = get_tempo_links()
    scraped_data = scrape_tempo_articles(tempo_links)
    filename = 'dataset_tempo.csv'
    write_to_csv(scraped_data, filename)
    print(f"Data has been written to {get_output_path(filename)}")

if __name__ == "__main__":
    main()
