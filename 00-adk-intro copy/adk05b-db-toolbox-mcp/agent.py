import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.toolbox_toolset import ToolboxToolset
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams 


load_dotenv()

instruction_prompt = """
        You are a helpful agent who can answer user questions about the hotels in a specific city or hotels by name. Use the tools to answer the question"
        """

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'travelexpert'
TOOLBOX_REMOTE_URL = os.genenv("TOOLBOX_REMOTE_URL")

##toolbox = ToolboxToolset(TOOLBOX_REMOTE_URL, toolset_name = "my_first_toolset")

connection_params=SseConnectionParams(
        url=f"{TOOLBOX_REMOTE_URL}/mcp/sse", 
        headers={}
)

mcp_toolset = MCPToolset(connection_params = connection_params)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about hotels in a city or hotels by name.",
        instruction=instruction_prompt,
        tools=[mcp_toolset]
)