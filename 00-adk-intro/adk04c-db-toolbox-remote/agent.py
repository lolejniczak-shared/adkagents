import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.toolbox_toolset import ToolboxToolset

load_dotenv()

TOOLBOX_REMOTE_URL = os.getenv("TOOLBOX_REMOTE_URL")

instruction_prompt = """
        You are a helpful agent who can answer user questions about the hotels in a specific city or hotels by name. Use the tools to answer the question"
        """

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'travelexpert'

toolbox = ToolboxToolset(TOOLBOX_REMOTE_URL, toolset_name = "my_first_toolset")

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about hotels in a city or hotels by name.",
        instruction=instruction_prompt,
        tools=[toolbox]
)