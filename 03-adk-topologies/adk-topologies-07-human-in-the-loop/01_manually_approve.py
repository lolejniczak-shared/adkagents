## need access to session - run from colab
import asyncio
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.events import Event, EventActions
import os

load_dotenv()

AGENT_APP_NAME = "agent"
USER_ID="user"
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
ADK_SESSION_ID = os.getenv('ADK_SESSION_ID')
DB_URL=os.getenv('DB_URL')


async def main():
    session_service = DatabaseSessionService(db_url=DB_URL)
    session = await session_service.get_session(app_name = AGENT_APP_NAME, 
                            session_id = ADK_SESSION_ID,
                            user_id = USER_ID
    )

    print(f"Current state: {session.state}")

    state_changes = {"decision": "approved"}
    actions_with_update = EventActions(state_delta=state_changes)
    system_event = Event(invocation_id="human_approval_request", author="system", actions=actions_with_update)

    ev = await session_service.append_event(session, system_event)

    updated_session = await session_service.get_session(
        app_name = AGENT_APP_NAME, 
        session_id = ADK_SESSION_ID,
        user_id = USER_ID
    )

    print(f"State after event: {updated_session.state}")


if __name__ == "__main__":
    asyncio.run(main())