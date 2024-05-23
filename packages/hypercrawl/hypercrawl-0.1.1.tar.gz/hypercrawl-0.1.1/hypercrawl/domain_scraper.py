# hypercrawl/domain_scraper.py
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

class DomainScraper:
    def __init__(self, base_url, max_concurrency=10, request_timeout=10):
        self.base_url = base_url
        self.visited = set()
        self.urls = set()
        self.max_concurrency = max_concurrency
        self.request_timeout = request_timeout

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=self.request_timeout) as response:
                if response.status == 200:
                    return await response.text()
        except asyncio.TimeoutError:
            print(f"Timeout fetching URL: {url}")
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
        return None

    async def crawl(self, session, url):
        if url in self.visited or not self.is_same_domain(url):
            return
        print(f"Crawling: {url}")
        self.visited.add(url)
        html = await self.fetch(session, url)
        if html:
            links = self.extract_links(html)
            tasks = []
            for link in links:
                full_link = urljoin(self.base_url, link)
                if self.is_valid_url(full_link) and self.is_same_domain(full_link):
                    tasks.append(self.crawl(session, full_link))
            if tasks:
                await asyncio.gather(*tasks)

            self.urls.add(url)

    async def get_all_urls_async(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=self.max_concurrency)) as session:
            await self.crawl(session, self.base_url)
        return self.urls

    def get_all_urls(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.get_all_urls_async())

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.base_url).netloc

    def extract_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links
