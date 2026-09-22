import requests
from bs4 import BeautifulSoup
from smolagents import DuckDuckGoSearchTool, tool
import re

# Standard search tool
web_search = DuckDuckGoSearchTool(max_results=5)


# --------------------------------------------------
# Tool 1: Search, Scrape & Filter 2026 news
# --------------------------------------------------
@tool
def search_and_scrape_2026(query: str) -> str:
    """
    Searches the web, visits links, and returns scraped text mentioning 2026.

    Args:
        query: What topic to search for.
    """
    # 1. Get search results
    search_results = web_search(f"{query} 2026")
    
    # 2. Extract URLs from the search results
    urls = re.findall(r"https?://[^\s)\]]+", search_results)
    
    if not urls:
        return "No links found. Try a different query."

    scraped_data = []

    # 3. Visit and scrape each page
    for url in urls[:2]:  # Scrape the first 2 links to keep it fast
        try:
            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Clean up unwanted HTML tags
            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            # Keep only if 2026 is mentioned
            if "2026" in text:
                # Take the first 500 characters so the model isn't overwhelmed
                scraped_data.append(f"Source ({url}):\n{text[:500]}...")
        except Exception:
            continue

    # 4. Fallback: If sites block scraping, return the raw search snippet
    if not scraped_data:
        if "2026" in search_results:
            return f"Websites protected from scraping. Using search snippets instead:\n\n{search_results}"
        return "No 2026 results found. Try a different query."

    return "\n\n---\n\n".join(scraped_data)

# --------------------------------------------------
# Tool 2: Evaluation Tool (Checks your research)
# --------------------------------------------------
@tool
def evaluate_sources(research: str) -> str:
    """
    Checks if research includes 2026 news and links.

    Args:
        research: The notes or search results found.
    """
    if "2026" not in research:
        return "Fix: Please make sure the news is from the year 2026."

    if "http" not in research:
        return "Fix: Please include at least one website link."

    return "Pass: Research looks good!"

# --------------------------------------------------
# Tool 3: Quality Check Tool (Checks the draft)
# --------------------------------------------------
@tool
def check_post_quality(post_text: str) -> str:
    """
    Checks if the LinkedIn post is clean, has hashtags, and asks a question.

    Args:
        post_text: The drafted LinkedIn post.
    """
    words = post_text.split()

    if len(words) < 50:
        return "Fix: Post is too short. Add more details."

    if "?" not in post_text:
        return "Fix: Add a question at the end to ask your readers."

    if "#" not in post_text:
        return "Fix: Add 3 hashtags at the bottom."

    return "Pass: Post is ready to share!"