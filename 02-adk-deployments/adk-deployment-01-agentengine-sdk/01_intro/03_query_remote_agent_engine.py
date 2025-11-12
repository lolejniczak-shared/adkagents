import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
import asyncio 

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"

AGENT_ENGINE_ID  = os.getenv('AGENT_ENGINE_ID')
AGENT_ENGINE_URI =f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
app = vertexai.agent_engines.get(AGENT_ENGINE_URI)

async def main():
    user_id = "u_456"

    remote_session = await app.async_create_session(user_id=user_id)
    print(remote_session)
    session_id=remote_session["id"]
    print(f"Created session: {session_id}")

    async for event in app.async_stream_query(
        user_id=user_id,
        session_id=session_id,
        message="Napisz cos ciekawego o systolic arrays",
    ):
        print(event)

if __name__ == "__main__":
    asyncio.run(main())