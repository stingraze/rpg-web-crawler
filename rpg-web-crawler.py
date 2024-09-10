# RPG Web Crawler - Version 0.1 by Tsubasa Kato - Inspire Search Corporation. 9/10/2024 9:01AM JST
# Created with the help of Perplexity Pro.
# How to use: python3 rpg-webcrawler.py https://www.example.com/some-url/
import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin, urlparse
import time
import sys
class RPGCrawler:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.traits = {
            "strength": 0,
            "intelligence": 0,
            "dexterity": 0,
            "charisma": 0,
            "wisdom": 0
        }
        self.keywords = {
            "strength": ["strong", "powerful", "muscle", "force", "might"],
            "intelligence": ["smart", "intelligent", "knowledge", "learn", "study"],
            "dexterity": ["agile", "quick", "nimble", "flexible", "swift"],
            "charisma": ["charming", "persuasive", "leadership", "confident", "attractive"],
            "wisdom": ["wise", "insightful", "experienced", "understanding", "perception"]
        }
        self.score = 0
        self.scoring_criteria = {
            "keyword_match": 1,
            "link_count": 0.5,
            "content_length": 0.01,
            "https": 5,
            "load_time": -0.1
        }

    def crawl(self):
        pages_crawled = 0
        urls_to_visit = [self.start_url]

        while urls_to_visit and pages_crawled < self.max_pages:
            url = urls_to_visit.pop(0)
            if url not in self.visited_urls:
                try:
                    page_score = self.visit_page(url)
                    self.score += page_score
                    pages_crawled += 1
                    print(f"Crawled {pages_crawled} pages. Current URL: {url}")
                    print(f"Page score: {page_score:.2f}")
                    self.display_traits()
                    self.display_score()
                    
                    new_urls = self.get_links(url)
                    urls_to_visit.extend(new_urls)
                except Exception as e:
                    print(f"Error crawling {url}: {str(e)}")

        print("Crawling complete!")
        self.display_traits()
        self.display_score()

    def visit_page(self, url):
        start_time = time.time()
        response = requests.get(url, timeout=5)
        load_time = time.time() - start_time
        self.visited_urls.add(url)
        
        page_score = 0
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Score based on keyword matches
            for trait, keywords in self.keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        self.traits[trait] += 1
                        page_score += self.scoring_criteria["keyword_match"]
            
            # Score based on link count
            links = soup.find_all('a', href=True)
            page_score += len(links) * self.scoring_criteria["link_count"]
            
            # Score based on content length
            page_score += len(text) * self.scoring_criteria["content_length"]
        
        # Score based on HTTPS
        if url.startswith("https"):
            page_score += self.scoring_criteria["https"]
        
        # Score based on load time
        page_score += load_time * self.scoring_criteria["load_time"]
        
        # Simulate "leveling up" with a random trait increase
        if random.random() < 0.1:  # 10% chance to level up
            trait = random.choice(list(self.traits.keys()))
            self.traits[trait] += random.randint(1, 3)
            print(f"Level up! {trait.capitalize()} increased!")

        return page_score

    def get_links(self, url):
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        valid_links = []
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            if self.is_valid_url(full_url):
                valid_links.append(full_url)
        
        return valid_links

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def display_traits(self):
        print("\nCurrent Traits:")
        for trait, value in self.traits.items():
            print(f"{trait.capitalize()}: {value}")
        print()

    def display_score(self):
        print(f"Total Score: {self.score:.2f}")
        print()

if __name__ == "__main__":
    #Start URL is argv[1]
    start_url = sys.argv[1]
    crawler = RPGCrawler(start_url, max_pages=20)
    crawler.crawl()
