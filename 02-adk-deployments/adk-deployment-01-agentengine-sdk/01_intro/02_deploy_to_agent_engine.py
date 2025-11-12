import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from vertexai.agent_engines import AdkApp
import asyncio 

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"

##------- our agent

root_agent = LlmAgent(
   name="basic_search_agent",
   model="gemini-2.5-flash", 
   description="Agent to answer questions using Google Search.",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search]
)

###------- our agent
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = AdkApp(
    agent=root_agent,
    enable_tracing=False,
)

remote_app = agent_engines.create(
    display_name = "Basic Search Agent with AdkApp",
    description = """
    This is basic ADK agent that generates answers using google search grounding
    """,
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform==1.126.1",
        "google-adk==1.18.0"
        ],
)