import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'bqassistant'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

bqcredentials = BigQueryCredentialsConfig(
        client_id = GOOGLE_CLIENT_ID, 
        client_secret = GOOGLE_CLIENT_SECRET
)

bqtoolset = BigQueryToolset(
        credentials_config=bqcredentials
)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Use BigQUery tools to handle user queries",
        instruction="You are helpful BigQuery assistant",
        tools = [bqtoolset]
)