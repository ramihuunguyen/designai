from crewai import Task

class TripTasks:

    def search_task(self, agent, query):
        return Task(
            description=f"Search the internet for the top  attractions, recommendations, or details regarding: {query}.",
            expected_output="A formatted list of 2 search results including titles, snippets, and links.",
            agent=agent
        )

    def scrape_task(self, agent, search_task_obj):
            
            return Task(
                description="Review the search results from the previous task, pick the most relevant URL, and scrape its webpage content to extract detailed travel insights.",
                expected_output= "A name of the place + when to go + 100 words only.",
                agent=agent,
                context=[search_task_obj]
            )