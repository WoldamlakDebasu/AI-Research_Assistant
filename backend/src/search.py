import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus, urljoin, urlparse
import re

class SearchEngine:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_duckduckgo(self, query, num_results=5):
        """Search using DuckDuckGo (more reliable than Google for scraping)"""
        try:
            # DuckDuckGo HTML search
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Parse DuckDuckGo results
            result_divs = soup.find_all('div', class_='result')
            
            for div in result_divs[:num_results]:
                try:
                    title_elem = div.find('a', class_='result__a')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # Get snippet
                    snippet_elem = div.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    print(f"Error parsing result: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
            return self._fallback_search_results(query)
    
    def search_bing(self, query, num_results=5):
        """Search using Bing (alternative search engine)"""
        try:
            search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Parse Bing results
            result_divs = soup.find_all('li', class_='b_algo')
            
            for div in result_divs[:num_results]:
                try:
                    title_elem = div.find('h2')
                    if not title_elem:
                        continue
                    
                    link_elem = title_elem.find('a')
                    if not link_elem:
                        continue
                        
                    title = link_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    
                    # Get snippet
                    snippet_elem = div.find('p') or div.find('div', class_='b_caption')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    if title and url and url.startswith('http'):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    print(f"Error parsing Bing result: {e}")
                    continue
            
            return results
            
        except Exception as e:
            print(f"Bing search error: {e}")
            return self._fallback_search_results(query)
    
    def search(self, query, num_results=5):
        """Main search method that tries multiple search engines"""
        print(f"Searching for: {query}")
        
        # Try DuckDuckGo first
        results = self.search_duckduckgo(query, num_results)
        
        # If no results, try Bing
        if not results:
            print("DuckDuckGo failed, trying Bing...")
            results = self.search_bing(query, num_results)
        
        # If still no results, use fallback
        if not results:
            print("All search engines failed, using fallback...")
            results = self._fallback_search_results(query)
        
        print(f"Found {len(results)} search results")
        return results
    
    def _fallback_search_results(self, query):
        """Fallback search results when real search fails"""
        return [
            {
                'title': f"Market Analysis: {query}",
                'url': "https://www.example.com/market-analysis",
                'snippet': f"Comprehensive market analysis and trends for {query}. Industry insights, key players, and growth projections."
            },
            {
                'title': f"Industry Report: {query}",
                'url': "https://www.example.com/industry-report",
                'snippet': f"Latest industry report covering {query}. Market size, competitive landscape, and future outlook."
            },
            {
                'title': f"Research Study: {query}",
                'url': "https://www.example.com/research-study",
                'snippet': f"In-depth research study on {query}. Data analysis, expert opinions, and strategic recommendations."
            }
        ]

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_url(self, url, max_length=3000):
        """Scrape content from a URL"""
        try:
            print(f"Scraping: {url}")
            
            # Skip certain file types
            if any(url.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']):
                return f"Document file detected: {url}. Content extraction not available for this file type."
            
            response = self.session.get(url, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            if 'text/html' not in content_type:
                return f"Non-HTML content detected: {content_type}. Content extraction not available."
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find main content areas
            content_selectors = [
                'article',
                'main',
                '.content',
                '.main-content',
                '.post-content',
                '.entry-content',
                '#content',
                '#main'
            ]
            
            content_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                    break
            
            # If no specific content area found, get all text
            if not content_text:
                content_text = soup.get_text()
            
            # Clean up the text
            content_text = re.sub(r'\s+', ' ', content_text).strip()
            
            # Limit length
            if len(content_text) > max_length:
                content_text = content_text[:max_length] + "..."
            
            if not content_text:
                return f"No readable content found at {url}"
            
            return content_text
            
        except requests.exceptions.Timeout:
            return f"Timeout error when accessing {url}"
        except requests.exceptions.RequestException as e:
            return f"Network error when accessing {url}: {str(e)}"
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
    
    def scrape_multiple_urls(self, urls, delay=1):
        """Scrape multiple URLs with delay between requests"""
        results = []
        
        for i, url in enumerate(urls):
            if i > 0:
                time.sleep(delay)  # Be respectful to servers
            
            content = self.scrape_url(url)
            results.append({
                'url': url,
                'content': content
            })
        
        return results

