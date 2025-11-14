import os
import google.adk
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agent.agent import root_agent
from google.genai import types
from google.adk.memory import VertexAiMemoryBankService
import asyncio

load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')

USER_ID="lolejniczak"

query = "Set temperature to my preferences?"

agent_engine_id = AGENT_ENGINE_RESOURCE_NAME.split("/")[-1]
print(agent_engine_id)
print(query)
memory_service = VertexAiMemoryBankService(
    project=PROJECT_ID,
    location=REGION,
    agent_engine_id=agent_engine_id
)

async def main():   
   memories = await memory_service.search_memory(query = query, app_name = AGENT_ENGINE_RESOURCE_NAME, user_id = USER_ID)

   for memory in memories:
       print(memory)

if __name__ == "__main__":
    asyncio.run(main())