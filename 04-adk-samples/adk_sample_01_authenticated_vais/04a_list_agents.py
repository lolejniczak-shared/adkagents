import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from agentspace_manager import AgentspaceManager

load_dotenv()

##PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
AGENT_ENGINE_ID = os.getenv('REASONING_ENGINE_ID')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
AGENTSPACE_APP_ID = os.getenv('AGENTSPACE_APP_ID')
AGENT_ENGINE_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
AGENT_AUTH_OBJECT_ID = os.getenv('AGENT_AUTH_OBJECT_ID')
AGENTSPACE_APP_NAME = os.getenv('AGENTSPACE_ADK_APP_NAME')

client = AgentspaceManager(project_id=PROJECT_ID,app_id=AGENTSPACE_APP_ID, location="global")


resp = client.list_agents()


agents = resp["agents"]
for agent in agents:
        print(agent)
        print(agent["name"])
        print(agent["displayName"])
        print("adk: -------------------------------")
        if agent.get("adkAgentDefinition"):
           print(agent["adkAgentDefinition"]["provisionedReasoningEngine"]["reasoningEngine"])
           print(agent["adkAgentDefinition"]["authorizations"])
        print("--------")

