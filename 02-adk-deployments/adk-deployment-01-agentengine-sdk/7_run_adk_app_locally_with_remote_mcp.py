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

# 3. Define an async main function
async def main():
    user_id = "u_456"
    try:
        # All your 'await' and 'async for' code goes inside here
        remote_session = await app.async_create_session(user_id=user_id)
        session_id = remote_session.id
        print(f"Created session: {remote_session.id}")

        async for event in app.async_stream_query(
            user_id=user_id,
            session_id=remote_session.id,
            message="Create post. Author Alice. text: Hello World. Sentiment should be positive",
        ):
            print(event)

        await mcpt.close()
        
    finally:
        # FIX #1: Ensure the session is closed to prevent the crash.
        if session_id:
                print("End of game ...")

# 4. Run the main async function
if __name__ == "__main__":
    asyncio.run(main())