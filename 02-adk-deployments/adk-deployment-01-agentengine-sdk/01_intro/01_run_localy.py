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
   model="gemini-2.5-flash", ### model that supports live streaming
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

# 3. Define an async main function
async def main():
    user_id = "u_456"
    # All your 'await' and 'async for' code goes inside here
    remote_session = await app.async_create_session(user_id=user_id)

    print(f"Created session: {remote_session.id}")

    async for event in app.async_stream_query(
        user_id=user_id,
        session_id=remote_session.id,
        message="Napisz cos ciekawego o systolic arrays",
    ):
        print(event)

# 4. Run the main async function
if __name__ == "__main__":
    asyncio.run(main())