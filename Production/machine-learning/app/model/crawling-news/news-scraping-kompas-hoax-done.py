import csv
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from scraper_config import get_output_path

# Function to write data to CSV file
def write_to_csv(data, filename):
    output_path = get_output_path(filename)
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(['id', 'title', 'source', 'url', 'image', 'date', 'content'])
        # Write data rows
        id_counter = 1
        for row in data:
            # Add id as first element and insert source and empty image
            processed_row = [id_counter, row[0], "Kompas", row[1], "", row[2], row[3]]
            writer.writerow(processed_row)
            id_counter += 1

# Get today's date for CSV
def get_date():
   return datetime.today().strftime('%Y-%m-%d')

# URL for next pages
def get_url(base_url, page):
   return f"{base_url}/{page}" if page > 1 else base_url
  
def extract_content(text):
    text = text.lower()

    # Words typically found at the beginning of news
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
    
# Main function to get data from Kompas hoax or fact
def get_data():
    # Get today's date to filter news
    today = get_date()
    data = []
    url = get_url('https://www.kompas.com/cekfakta/hoaks-atau-fakta', 1)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    news_items = soup.find_all('a', class_='cekfakta-list-link')
    for item in news_items:
        # Check news date
        date_elem = item.find('p', class_='cekfakta-text-date')

        date_str = date_elem.get_text(strip=True).split(',')[0]
        # Convert to YYYY-MM-DD format
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            formatted_date = today  # Fallback to today if parsing fails
            
        # Skip if older than today
        if formatted_date != today:
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
        processed_content = extract_content(content)

        data.append([title, link, formatted_date, processed_content])
    return data

def main():
    processed_data = get_data()
    filename = 'dataset_kompas_hoaks.csv'
    write_to_csv(processed_data, filename)
    print(f"Data has been written to {get_output_path(filename)}")

if __name__ == '__main__':
    main()