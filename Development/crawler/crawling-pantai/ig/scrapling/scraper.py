from scrapling.fetchers import Fetcher, AsyncFetcher, StealthyFetcher, PlayWrightFetcher
StealthyFetcher.auto_match = True
# Fetch websites' source under the radar!
page = StealthyFetcher.fetch('https://www.instagram.com/explore/search/keyword/?q=%23pantaisanur', 
                             headless=True, 
                             network_idle=5000,
                             wait_selector='div',)
print(page.status)
div = print(page.find_all('div'))