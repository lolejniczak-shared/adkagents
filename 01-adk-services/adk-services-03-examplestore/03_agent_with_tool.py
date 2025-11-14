## need access to session - run from colab
import asyncio
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import requests
from agent_without_examplestore.agent import root_agent

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



async def main():
    # Create InMemory services for session and artifact management
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()


    session = await session_service.create_session(
        app_name = AGENT_APP_NAME, 
        user_id = "testuser", 
    )

    runner = Runner(app_name=AGENT_APP_NAME, 
            agent=root_agent, 
            artifact_service=artifact_service,
            session_service=session_service)


    ## test
    question = "What is the latest exchange rate from polish Zloty to US dollars?"
    resp = await get_response(runner, session.user_id ,session.id, question)
    print(resp)

if __name__ == "__main__":
    asyncio.run(main())

##FunctionCall
##FunctionResponse
##FinalModelResponse