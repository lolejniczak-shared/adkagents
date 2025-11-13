## need access to session - run from colab
import asyncio
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'basic_agent'

async def get_response(runner, user_id, session_id,  message):
    content = types.Content(role='user', parts=[types.Part(text=message)])
    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)
    final_response = None
    for _, event in enumerate(events):
        is_final_response = event.is_final_response()
        if is_final_response:
            final_response = event.content.parts[0].text
    return final_response


root_agent = Agent(
        model="gemini-2.5-flash",
        name='user_assistant',
        instruction="""
        You are helpful assistant. Your role is to answer user questions.
        Current user:
            <User>
            {user_info}
            </User>
            Current time: {time}.

        """,
        tools=[]
    )