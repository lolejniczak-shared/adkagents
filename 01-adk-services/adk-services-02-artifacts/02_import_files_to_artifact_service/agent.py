from google.adk.tools import agent_tool
from google.adk.agents import LlmAgent, BaseAgent
from google import genai
from google.adk.events import Event
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.tools import google_search  # Import the tool
from functools import partial
from typing import Optional
from google.genai import types
import copy

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import LlmRequest, LlmResponse
from google.adk.artifacts import GcsArtifactService
from google import genai
from google.genai.types import Part

import os

import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from vertexai import agent_engines

load_dotenv()

ARTIFACT_BUCKET_NAME = "lolejniczak-adk-artifacts-service"
PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=f'gs://lolejniczak-adk-training'
)

async def list_user_files_py(tool_context: ToolContext) -> str:
    """Tool to list available artifacts for the user."""
    try:
        available_files = await tool_context.list_artifacts()
        if not available_files:
            return "You have no saved artifacts."
        else:
            # Format the list for the user/LLM
            file_list_str = "\n".join([f"- {fname}" for fname in available_files])
            return f"Here are your available Python artifacts:\n{file_list_str}"
    except ValueError as e:
        print(f"Error listing Python artifacts: {e}. Is ArtifactService configured?")
        return "Error: Could not list Python artifacts."
    except Exception as e:
        print(f"An unexpected error occurred during Python artifact list: {e}")
        return "Error: An unexpected error occurred while listing Python artifacts."


list_files_tool = FunctionTool(func=list_user_files_py)


async def save_uploaded_files_to_artifacts_service(
    callback_context, llm_request
):
    invocation_context = callback_context._invocation_context
    artifact_service = callback_context._invocation_context.artifact_service
    
    user_content = callback_context._invocation_context.user_content
    print(user_content)
    if not user_content.parts:
       return None

    new_parts = []

    for i, part in enumerate(user_content.parts):
            ## if there is no inline_data --> nothing was uploaded -- just continue
            if part.inline_data is None:
                continue

            try:
                # Use display_name if available, otherwise generate a filename
                file_name = part.inline_data.display_name
                if not file_name:
                    file_name = f'artifact_{invocation_context.invocation_id}_{i}'
                    print(
                        f'No display_name found, using generated filename: {file_name}'
                    )

                # Store original filename for display to user/ placeholder
                display_name = file_name

                # Create a copy to stop mutation of the saved artifact if the original part is modified
                await invocation_context.artifact_service.save_artifact(
                    app_name=invocation_context.app_name,
                    user_id=invocation_context.user_id,
                    session_id=invocation_context.session.id,
                    filename=file_name,
                    artifact=copy.copy(part),
                )

                
            except Exception as e:
                print(f'Failed to save artifact for part {i}: {e}')
                continue
    return None



root_agent = LlmAgent(
    name='root_agent',
    model='gemini-2.5-flash',
    before_model_callback = save_uploaded_files_to_artifacts_service,
    tools = [list_files_tool, load_artifacts]
)