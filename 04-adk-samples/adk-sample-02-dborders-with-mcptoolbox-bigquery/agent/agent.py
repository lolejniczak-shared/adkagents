import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.toolbox_toolset import ToolboxToolset
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams 
from google.adk.tools.toolbox_toolset import ToolboxToolset

load_dotenv()

instruction_prompt = """
        You are a helpful shopping assistant. Use available tools to describe existing and create new orders"
        """

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'order_assistant'

#####https://cloud.google.com/run/docs/host-mcp-servers#authenticate_mcp_clients

connection_params=SseConnectionParams(
        url="https://dbtoolbox4orderswithbq-680248386202.us-central1.run.app/mcp/sse", 
        ##url="http://localhost:5000/mcp/sse", 
        headers={}
)

mcp_toolset = MCPToolset(connection_params = connection_params)


##mcp_toolset = ToolboxToolset("http://localhost:5000", toolset_name = "my_first_toolset")

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions orders and products",
        instruction=instruction_prompt,
        tools=[mcp_toolset]
)