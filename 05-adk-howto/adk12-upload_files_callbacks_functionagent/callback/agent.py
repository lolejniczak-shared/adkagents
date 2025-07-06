import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional
from google.genai import types 
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
from .function_agent import FunctionAgent

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'enterpriseagent'


@FunctionAgent(name="data_collection", model = MODEL)
async def data_collection(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    # Inspect the last user message in the request contents
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        index_i = 0
        for content in llm_request.contents:
            
            for part in content.parts:
                if part.inline_data: ##or part.file_data:
                    print("image")
                    print(part)
                    report_artifact = types.Part.from_bytes(
                                data=part.inline_data.data,
                                mime_type=part.inline_data.mime_type
                    )
                    callback_context.state[f"worker{index_i}"]=part.inline_data.display_name
                    artifact = await callback_context.save_artifact(filename=part.inline_data.display_name, artifact=report_artifact)
                elif part.text:
                    print(part.text)
                    callback_context.state["question"]=part.text
                else: 
                    print("other")
                index_i += 1
    

    return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="Uploaded artifacts were added to artifacts service and session state")],
            )
        )

report_generator = LlmAgent(
        model=MODEL,
        name="report_generator",
        description="Compile document summarizations into final report",
        instruction="Compile document summarizations into final report",
        include_contents = 'none' ### so that it does not add artifacts again
)

root_agent = SequentialAgent(
    name = "report_generation_workflow",
    sub_agents = [data_collection, report_generator]
)








