import csv
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

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

def scrape_tempo_articles(tempo_links):
    data = []
    date = get_date()
    
    for title, link in tempo_links:
        category, title_news = title.split(':', 1) if ':' in title else (title, title)
        is_fake = 1 if category in ["Menyesatkan", "Keliru"] else 0
        
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        detail_in = soup.find('div', 'detail-in')
        p = detail_in.find_all('p')
        content = ' '.join(p.get_text() for p in p)
        
        data.append([title_news, link, date, content, is_fake])
    
    return data

def write_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'link', 'date', 'content', 'is_fake'])
        writer.writerows(data)

def extract_content(text):
    match = re.search(r"(jakarta -|jakarta-)(.*)", text.lower(), re.DOTALL)
    return match.group(2).strip() if match else text

def process_raw(filename):
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        modified_data = [[row['title'], row['link'], row['date'], extract_content(row['content']), row['is_fake']] for row in reader]
    
    write_to_csv(modified_data, 'dataset_tempo.csv')
    print("Data has been written to dataset_tempo.csv")

def main():
    filename = 'dataset_tempo_raw.csv'
    tempo_links = get_tempo_links()
    scraped = scrape_tempo_articles(tempo_links)
    write_to_csv(scraped, filename)
    print(f"Data has been written to {filename}")
    process_raw(filename)

if __name__ == "__main__":
    main()
