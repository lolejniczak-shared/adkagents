import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.bigquery import BigQueryToolset

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'bqassistant'

bqtoolset = BigQueryToolset()

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Use BigQUery tools to handle user queries",
        instruction="You are helpful BigQuery assistant",
        tools = [bqtoolset]
)