import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

load_dotenv()

async def auto_save_session_to_memory_callback(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session)

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name='stateful_agent',
    instruction="""You are Helpful HomeAssistant. You dont have tools so always assume you are able to use hypithetical tool representing the living room thermostat.""",
    tools=[PreloadMemoryTool()],
    after_agent_callback=auto_save_session_to_memory_callback
)