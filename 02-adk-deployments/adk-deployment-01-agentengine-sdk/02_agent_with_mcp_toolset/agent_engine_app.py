import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from vertexai.agent_engines import AdkApp
from vertexai.agent_engines import ModuleAgent
import asyncio
from agent_remote_mcp.agent import root_agent
from agent_remote_mcp.agent import mcpt
from google.adk.sessions.in_memory_session_service import InMemorySessionService

def session_service_builder():
  """Builds the session service to use in the ADK app."""
  # This is needed to ensure InitGoogle and AdkApp setup is called first.
  from google.adk.sessions.in_memory_session_service import InMemorySessionService
  return InMemorySessionService()

adkapp = AdkApp(
    agent=root_agent,
    ##enable_tracing=True,
    ##session_service_builder=session_service_builder, ##playground does not work with in memory session service
)