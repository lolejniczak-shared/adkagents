from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'

generator = LlmAgent(
    model=MODEL,
    name="DraftWriter",
    instruction="You are science journalist. Write draft of article for topic from the customer.",
    description="Agent that is responsible for generating articles",
    output_key="draft_text"
)

reviewer = LlmAgent(
    model=MODEL,
    name="Critique",
    instruction="""Review the following draft: 
    ***DRAFT:
    {draft_text}
    
    Assess factual accuracy. 
    Specify what should be improved. Output 'valid' or 'invalid' with reasons.""",
    description="Agent that is responsible for constructive critique of the provided text",
    output_key="review_status",
    tools=[google_search]
)

# Optional: Further steps based on review_status

writer_agent = SequentialAgent(
    name="WriteAndReview",
    sub_agents=[generator, reviewer]
)

root_agent = writer_agent