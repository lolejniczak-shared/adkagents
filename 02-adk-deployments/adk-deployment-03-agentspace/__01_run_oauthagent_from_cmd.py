## need access to session - run from colab
import asyncio
from agentoauth import agent as oagent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import sys
import importlib

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'basic_agent'

async def get_response(runner, user_id, session_id,  message):
    content = types.Content(role='user', parts=[types.Part(text=message)])
    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)
    final_response = None
    for _, event in enumerate(events):
        print(event)
        is_final_response = event.is_final_response()
        if is_final_response:
            final_response = event.content.parts[0].text
    return final_response

def get_auth_token() -> str:
    """
    Gets a Google-signed OAuth 2.0 access token for authentication.
    """
    print("Getting authentication token...")
    try:
        # Get the default credentials from the environment (from 'gcloud auth')
        credentials, _ = google_auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform",
                "openid",
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/drive.metadata"]
        )
        # Refresh the credentials to get a valid token
        auth_request = google_requests.Request()
        credentials.refresh(auth_request)
        print("Successfully obtained auth token.")
        return credentials.token
    except Exception as e:
        print(f"FATAL: Could not get Google credentials. "
              f"Please run 'gcloud auth application-default login'. Error: {e}")
        raise


async def main():
    # Create InMemory services for session and artifact management
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    agent = oagent.root_agent
    access_token= get_auth_token()

    _state = {
            ##"temp:http_1754759092029979798__existing_exchanged_credential": get_auth_token()
            "temp:adk_http_-2077203557243113090_": access_token ##get_auth_token()
    }
    print(_state)

    session = await session_service.create_session(app_name = AGENT_APP_NAME, 
                            user_id = "testuser", 
                            state = _state)

    runner = Runner(app_name=AGENT_APP_NAME, 
            agent=agent, 
            artifact_service=artifact_service,
            session_service=session_service)


    ## test
    ##resp = await get_response(runner, session.user_id ,session.id, "describe session state")
    resp = await get_response(runner, session.user_id ,session.id, "show my gdrive files")
    print(resp)

if __name__ == "__main__":
    asyncio.run(main())