import os
from dotenv import load_dotenv
from crewai import Crew, Process
from trip_agents import TripAgents
from trip_tasks import TripTasks

# Load environment variables
load_dotenv()

# Instantiate agents and tasks
agents = TripAgents()
tasks = TripTasks()

# Define the trip destination query
destination_query = "Select the place in Singapore."

# Create agents
researcher = agents.research_agent()
scraper = agents.content_agent()

# Create tasks
t1 = tasks.search_task(agent=researcher, query=destination_query)
t2 = tasks.scrape_task(agent=scraper, search_task_obj=t1)

# Assemble and run the Crew
boston_trip_crew = Crew(
    agents=[researcher, scraper],
    tasks=[t1, t2],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":

    print("## Welcome to the Boston Trip Planning Crew ##")
    print("-----------------------------------------------")

    result = boston_trip_crew.kickoff()

    print("\n\n########################")
    print("## Here is your result:")
    print("########################\n")

    print(result)