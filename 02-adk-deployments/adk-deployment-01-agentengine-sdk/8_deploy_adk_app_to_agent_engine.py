import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from vertexai.agent_engines import AdkApp
from vertexai.agent_engines import ModuleAgent
import asyncio
from agent_remote_mcp.agent.agent import root_agent
from agent_remote_mcp.agent.agent import mcpt

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"


vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)


app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    display_name = "InstaVibe agent with AdkApp",
    description = """
    This is basic ADK agent that communicates with InstaVive backend
    """,
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform==1.126.1",
        "google-adk==1.18.0"
        ],
)