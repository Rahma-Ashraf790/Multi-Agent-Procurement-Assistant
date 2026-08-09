import os
import re
import json
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from tavily import TavilyClient
from crewai.tools import BaseTool

load_dotenv()

# Settings
TAVILY_MAX_RESULTS = 3
MAX_SCRAPER_URLS = 2

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search"
    description: str = "Search the web for products and return names, prices, specs and URLs."

    def _run(self, query: str) -> str:
        try:
            response = tavily_client.search(query=query, max_results=TAVILY_MAX_RESULTS)
            results = response.get("results", [])
            simplified = [
                {"title": i.get("title"), "url": i.get("url"), "content": i.get("content")}
                for i in results
            ]
            return json.dumps(simplified, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"Search error: {str(e)}"

class ProductScraperTool(BaseTool):
    name: str = "Product Page Scraper"
    description: str = "Scrapes product URLs. Input: comma-separated URLs."

    def _run(self, urls: str) -> str:
        url_list = [u.strip() for u in str(urls).split(",") if u.strip().startswith("http")][:MAX_SCRAPER_URLS]
        if not url_list:
            return "No valid URLs provided."
        results = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0"}
        for url in url_list:
            item = {"url": url, "success": False}
            try:
                response = requests.get(url, headers=headers, timeout=20)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    title_tag = soup.find("meta", attrs={"property": "og:title"})
                    if title_tag and title_tag.get("content"):
                        item["name"] = title_tag["content"].strip()
                    elif soup.title and soup.title.string:
                        item["name"] = soup.title.string.strip()
                    price_tag = soup.find("meta", attrs={"itemprop": "price"}) or soup.find("meta", attrs={"property": "product:price:amount"})
                    if price_tag and price_tag.get("content"):
                        item["price"] = price_tag["content"].strip()
                    for tag in soup(["script", "style", "nav", "footer", "header"]):
                        tag.decompose()
                    text = re.sub(r"\s+", " ", soup.get_text(separator=" ", strip=True))
                    item["specs_snippet"] = text[:2000]
                    item["success"] = True
                else:
                    item["error"] = f"HTTP {response.status_code}"
            except Exception as e:
                item["error"] = str(e)
            results.append(item)
        return json.dumps(results, ensure_ascii=False)[:8000]

# Create tools
search_tool = TavilySearchTool()
scraper_tool = ProductScraperTool()