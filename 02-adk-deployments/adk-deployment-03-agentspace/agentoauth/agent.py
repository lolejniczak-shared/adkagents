import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search  # Import the tool
from functools import partial
from typing import Optional
from google.genai import types
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from fastapi.openapi.models import OAuth2, HTTPBearer
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.auth.auth_credential import HttpAuth
from google.adk.auth.auth_credential import HttpCredentials
from google.adk.events import Event
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
PROJECT_ID=os.environ["ADK_CLOUD_PROJECT"]
LOCATION=os.environ["ADK_CLOUD_LOCATION"]
APPLICATION_INTEGRATION_LOCATION = "europe-central2"


async def dump_state(tool_context: 'ToolContext'):
        """describe session state"""
        state_dict = tool_context.state.to_dict()
        print("Dumping session state:")
        result = "Dumping session state:"
        for key, value in state_dict.items():
                state = f"{key}: {value}"
                result += state  

        return Event(content=types.Content(parts=[types.Part(text=result)], 
            role='model'), 
            author="model")


##tool_auth_handler.py
auth_scheme = HTTPBearer(
        ##bearerFormat="JWT"
)
auth_credential = None

gdrive_connection_toolset = ApplicationIntegrationToolset(
            project=PROJECT_ID, 
            location=APPLICATION_INTEGRATION_LOCATION, 
            connection="gdrive-connector-with-auth", 
            entity_operations={},
            actions=["GET_files"], 
            ##service_account_credentials='{...}', 
            tool_name_prefix="mygdrive",
            tool_instructions="Use this tool to work with gdrive",
            auth_credential=auth_credential, ##auth_credential,
            auth_scheme=auth_scheme ##auth_scheme
 )


def simple_before_tool_modifier(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """Inspects/modifies tool args or skips the tool call."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")


    state_dict = tool_context.state.to_dict()
    for key, value in state_dict.items():
        if key.startswith("temp:"):
           key_without_temp_prefix = f"adk_{key[len('temp:'):]}"
           tool_context.state[f"{key_without_temp_prefix}"] = value
           print(f"[Callback] Updated key in state: {key_without_temp_prefix}")
    return None

root_agent = LlmAgent(
   name="basic_search_agent",
   model="gemini-2.0-flash-001", ### model that supports live streaming
   description="Agent to answer questions using available tools",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[dump_state, gdrive_connection_toolset],
   ##before_agent_callback=partial(update_ui_status, status_msg="Starting handling user question"),
   ##after_agent_callback=partial(update_ui_status, status_msg="Answer generation complete"),
   before_tool_callback=simple_before_tool_modifier
)