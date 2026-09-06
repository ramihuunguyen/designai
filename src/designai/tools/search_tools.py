import json
import os
import sys
import requests
from crewai.tools import tool
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
serpapi_key = os.environ['SERPAPI_API_KEY']

class SearchTools:

    @tool("Search the internet")

    def search_google(query: str) -> str:
        """Search the internet about a user topic and return the top 4 results."""
        params = {"engine": "google", "q": query, "api_key": serpapi_key, "num": 4}
        results = GoogleSearch(params).get_dict()
        
        # Collect top organic results up to 4 items
        organic = results.get("organic_results", [])

        if organic:
            
            formatted_results = []
            for item in organic[:4]:

                title = item.get("title", "No Title")

                snippet = item.get("snippet", "No description available.")

                link = item.get("link", "No link available.")

                formatted_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
            
            return "\n".join(formatted_results)
            
        return "No results."

#Test
#result = SearchTools.search_internet.run(query="where is Boston?")
#print(result)