#Agent 1: Build my trip planning agent
#Developer: Rami Huu Nguyen
#Date: Sep 5th, 2026

from crewai import Agent, LLM
from langchain_openai import OpenAI
from tools.search_tools import SearchTools
from tools.scrape_tools import ScrapeTools
import os

openrouter_llm = LLM(
    model="openrouter/openai/gpt-4o-mini",  
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

class TripAgents:
    
    def research_agent(self):
        return Agent(

            role='Destination Researcher',

            goal='Find the best attractions, restaurants, and hidden spots using web searches.',

            backstory='An expert travel researcher with an eye for detail, skilled at gathering top recommendations.',

            tools=[SearchTools.search_google],

            llm=openrouter_llm,

            verbose=True
        )

    def content_agent(self):

        return Agent(
            role='Content Scraper and Summarizer',

            goal='Extract and summarize detailed information from official travel and guide URLs.',

            backstory='A precise editor who reads through raw webpage content to pull out essential travel facts.',

            tools=[ScrapeTools.scrape_url],

            llm=openrouter_llm,

            verbose=True
        )