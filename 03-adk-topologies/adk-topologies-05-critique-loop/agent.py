from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from pydantic import BaseModel
from pydantic import Field
import json


load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'

async def init_state(callback_context: CallbackContext):
    callback_context.state["draft_text"] = "Not available"
    callback_context.state["feedback"] = "Not available"
    callback_context.state["article_status"] = "invalid"
    return None


generator = LlmAgent(
    model=MODEL,
    name="DraftWriter",
    instruction="""You are science journalist and write articles for a user. 
    Use draft text and feedback: 
    ***DRAFT: 
    {draft_text}
    ***FEEDBACK: {feedback}. 
   
    Write draft taking into account provided feedback (if present). 
    """,
    description="Agent that is responsible for generating articles.",
    output_key="draft_text",
    before_agent_callback = init_state
)

reviewer = LlmAgent(
    model=MODEL,
    name="Critique",
    instruction="""Review draft of the article in {draft_text} for factual scientific accuracy and how informative it is to the target audience. 
    Specify what should be improved. """,
    description="Agent that is responsible for constructive critique of the provided text",
    output_key="feedback",
    tools=[google_search]
)

class ArticleStateSchema(BaseModel):
    article_state: str = Field(description="Decision on the status of article draft as valid or invalid")

manager = LlmAgent(
    model=MODEL,
    name="Feedback",
    instruction="""Review feedback: {feedback}.
    Check if feedback suggests that next iteration of drafting text is needed. If no further changes are needed set review status to "valid". Otherwise set is as "invalid".
    """,
    description="Agent that is responsible for checking feedback",
    output_key="article_status",
    output_schema=ArticleStateSchema
)



class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        print(f"--------------------")
        s = ctx.session.state.get("article_status")
        status = s["article_state"]
        print(f"Status: {status}")
        should_stop = (status == "valid")
        print(f"Should stop: {should_stop}")
        print(f"--------------------")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

writing_loop = LoopAgent(
    name="WritigRefinementLoop",
    max_iterations=5,
    sub_agents=[generator, reviewer, manager, CheckStatusAndEscalate(name="StopChecker")],
)



root_agent = LlmAgent(
    model=MODEL,
    name="coordinator",
    instruction="""You help users write articles""",
    description="Agent that is responsible for communication with users",
    sub_agents = [writing_loop]
)

