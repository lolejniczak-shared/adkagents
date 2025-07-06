import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional
from google.genai import types 
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'enterpriseagent'

async def simple_before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

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

collect_user_data = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Model execution is skipped",
        instruction="Do nothing",
        before_model_callback=simple_before_model_modifier
)

report_generator = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Compile document summarizations into final report",
        instruction="Compile document summarizations into final report",
        include_contents = 'none' ### so that it does not add artifacts again
)

async def append_artifacts_to_llm_request(
      callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    artifact_name = callback_context.state.get(agent_name)
    if artifact_name: 
        artifact = await callback_context.load_artifact(artifact_name)
        if artifact: 
            llm_request.contents.append(
                    types.Content(
                        role='user',
                        parts=[
                            types.Part.from_text(
                                text=f'Artifact {artifact_name} is:'
                            ),
                            artifact,
                        ],
                    )
                )
        else:
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="No artifact available")],
                )
            )
    else:
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="No artifact available")],
            )
        )


number_of_workers = 4
workers = []
for i in range(number_of_workers):

    doctor = Agent(name=f"worker{i}", 
    model = MODEL, 
    instruction=f"""
    Generate detailed description of the provided artifact. 
    Display state['worker{i}']:
    Output:
    artifact_name: {{state['worker{i}']}}
    artifact_description:  
    """, 
    output_key=f"artifact_summary_{i}",
    before_model_callback=append_artifacts_to_llm_request
    )
    workers.append(doctor)

parallel_workers = ParallelAgent(
    name="ParallelAssesment",
    sub_agents=workers
)

root_agent = SequentialAgent(
    name = "report_generation_workflow",
    sub_agents = [collect_user_data, parallel_workers, report_generator]
)