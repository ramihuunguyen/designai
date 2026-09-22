import os
import gradio as gr
from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool

# Import your tools from tools.py
from tools import evaluate_sources, check_post_quality, search_and_scrape_2026

load_dotenv(".env")
HF_TOKEN = os.getenv("HF_TOKEN")

# Setup Model and Search Tool
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HF_TOKEN
)

# Connect agent to all 3 tools
agent = CodeAgent(
    tools=[search_and_scrape_2026, evaluate_sources, check_post_quality],
    model=model,
    max_steps=10,
)

def make_linkedin_post(topic: str) -> str:
    if not topic.strip():
        return "Please enter a topic first."

    prompt = f"""
Write a great LinkedIn post about: {topic}

Please do these 4 easy steps:

1. Search for 2026 news on this topic.
2. Run evaluate_sources to make sure the news is from 2026.
3. Write the post: clear hook, 3 short bullet points, a question for comments, and 3 hashtags.
4. Run check_post_quality to test the post before finishing.

"""
    return str(agent.run(prompt))

# Launch Gradio
demo = gr.Interface(

    fn=make_linkedin_post,
    inputs=gr.Textbox(label="Topic", placeholder="e.g. AI tools in 2026"),
    outputs=gr.Markdown(label="Final LinkedIn Post"),
    title="Simple LinkedIn Post Creator"
)

if __name__ == "__main__":
    demo.launch()