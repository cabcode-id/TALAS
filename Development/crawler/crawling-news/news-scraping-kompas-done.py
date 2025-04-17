import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sys
import csv
from scraper_config import get_output_path

def extract_article_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cari element dengan tag p terbanyak
        p_tag_counts = {}
        for elem in soup.find_all():
            p_tags = elem.find_all('p')
            if p_tags:
                p_tag_counts[elem] = len(p_tags)
        
        if not p_tag_counts:
            print(f"No <p> tags found in {url}")
            return ""
        
        content_elem = max(p_tag_counts.items(), key=lambda x: x[1])[0]
        
        # Ekstrak teks dari setiap p tag kecuali yang <strong>
        content_parts = []
        for p in content_elem.find_all('p'):
            for strong in p.find_all('strong'):
                strong.unwrap() 
            
            text = p.get_text(strip=True)
            if text:
                content_parts.append(text)
        
        return ' '.join(content_parts)
        
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return ""

def save_to_csv(articles_data, filename="kompas_news.csv"):
    """Save article data to CSV file"""
    output_path = get_output_path(filename)
    fieldnames = ['id', 'title', 'source', 'url', 'image', 'date', 'content']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, article in enumerate(articles_data, 1):
            writer.writerow({
                'id': i,
                'title': article['title'],
                'source': 'Kompas',
                'url': article['link'],
                'image': '',
                'date': article['date'],
                'content': article['content']
            })
    
    print(f"Saved {len(articles_data)} articles to {output_path}")

def scrape_kompas_news():
    today = datetime.now()
    date_for_url = today.strftime("%Y-%m-%d")  # URL format: 2025-03-14
    date_for_comparison = today.strftime("%Y-%m-%d")  # Database format: 2025-03-14
        
    articles_data = []  #  store dictionaries of article data
    all_articles = []  #  store tuples of (link, title)
    
    # First, get the total number of pages
    url = f"https://indeks.kompas.com/?site=news&date={date_for_url}&page=1"
    print(f"Getting pagination info from: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Cari nomor halaman maksimal ada berapa
        pagination_div = soup.select_one('.paging__wrap')
        if pagination_div:
            print(f"Found pagination container: {pagination_div.name} with class {pagination_div.get('class')}")
            page_links = pagination_div.select('.paging__link')
            print(f"Found {len(page_links)} pagination links")
            for link in page_links:
                print(f"Page link: {link.get('href')} - Text: {link.text}")
        else:
            print("No pagination container found")
        
        last_page_link = soup.select_one('.paging__link--last')
        
        if not last_page_link:
            page_links = soup.select('.paging__link')
            if page_links:
                page_numbers = []
                for link in page_links:
                    try:
                        page_num = int(link.text.strip())
                        page_numbers.append(page_num)
                    except ValueError:
                        continue
                if page_numbers:
                    last_page = max(page_numbers)
                    print(f"Determined last page from link text: {last_page}")
                else:
                    last_page = 1
            else:
                last_page = 1
        else:
            if 'page=' in last_page_link.get('href', ''):
                last_page = int(last_page_link.get('href').split('page=')[-1])
                print(f"Found last page link: {last_page_link}")
            else:
                last_page = 1
            
        print(f"Found {last_page} pages to scrape")
        
        # iterate through all pages
        for page in range(1, last_page + 1):
            url = f"https://indeks.kompas.com/?site=news&date={date_for_url}&page={page}"
            print(f"Scraping page {page}/{last_page}: {url}")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all article cards/containers
            article_containers = soup.select('.articleListItem')
            if article_containers:
                print(f"Found {len(article_containers)} articles with .articleListItem selector")
            
            if not article_containers:
                # Try an alternative selector if the first one doesn't work
                article_containers = soup.select('.article__asset')
                if article_containers:
                    print(f"Found {len(article_containers)} articles with .article__asset selector")
            
            if not article_containers:
                # Try another possible class
                article_containers = soup.select('.latest--indeks')
                if article_containers:
                    print(f"Found {len(article_containers)} articles with .latest--indeks selector")
            
            if not article_containers:
                print(f"No article containers found on page {page}. Trying to find any links...")
                # As a fallback, look for any links with article titles
                article_containers = soup.select('a[href*="kompas.com/read/"]')
                if article_containers:
                    print(f"Found {len(article_containers)} articles with direct link selector")
            
            page_articles = []
            
            for container in article_containers:
                article_link = None
                article_title = None
                
                # If the container is already a link
                if container.name == 'a' and container.get('href'):
                    article_link = container.get('href')
                    title_elem = container.select_one('h2') or container.select_one('.article__title') or container
                    article_title = title_elem.get_text(strip=True)
                else:
                    # Find the link within the container
                    link_elem = container.select_one('a[href*="kompas.com/read/"]')
                    if link_elem:
                        article_link = link_elem.get('href')
                        title_elem = container.select_one('h2') or container.select_one('.article__title') or link_elem
                        article_title = title_elem.get_text(strip=True)
                
                if article_link and article_title:
                    page_articles.append((article_link, article_title))
            
            print(f"Successfully extracted {len(page_articles)} articles on page {page}")
            all_articles.extend(page_articles)
            
            # Add a delay between page requests
            time.sleep(5)
            
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"Total articles found across all pages: {len(all_articles)}")
    
    # Extract content from each article
    print("\nExtracting content from each article...")
    for i, (link, title) in enumerate(all_articles, 1):
        print(f"Processing article {i}/{len(all_articles)}: {title}")
        content = extract_article_content(link)
        
        articles_data.append({
            'title': title,
            'link': link,
            'date': date_for_comparison,
            'content': content
        })
        
        # Add a small delay to avoid overloading the server
        time.sleep(1)
    
    # Save the collected data to CSV
    save_to_csv(articles_data)
    
    return articles_data

if __name__ == "__main__":
    articles = scrape_kompas_news()
    
    # Print summary of collected articles
    print("\nSummary of collected articles:")
    for i, article in enumerate(articles, 1):
        title = article['title'] if article['title'] else "[No title found]"
        content_preview = article['content'][:100] + "..." if len(article['content']) > 100 else article['content']
        print(f"{i}. {title}")
        print(f"   Content preview: {content_preview}")
        print()
