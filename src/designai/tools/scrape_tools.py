import json
import os
import sys
import requests
from crewai.tools import tool
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

serpapi_key = os.environ['SERPAPI_API_KEY']
#print(serpapi_key)
#sys.exit()

class ScrapeTools:

    @tool("Scrape website content")
    def scrape_url(url: str) -> str:
        """Scrape text content from a specific URL to analyze or summarize."""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        paragraphs = soup.find_all('p')
        text_content = " ".join([p.get_text() for p in paragraphs])
        cleaned_text = " ".join(text_content.split())
        
        return cleaned_text[:2000] + "..." if len(cleaned_text) > 2000 else cleaned_text

#Test
#sample_url = "https://en.wikipedia.org/wiki/Boston"
#scrape_output = ScrapeTools.scrape_url.run(url=sample_url)
#print(scrape_output)