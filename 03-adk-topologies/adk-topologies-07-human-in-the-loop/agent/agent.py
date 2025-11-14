from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search
from google.adk.tools import agent_tool
from pydantic import BaseModel
from pydantic import Field
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any
from typing import Optional
from google.adk.models import LlmResponse, LlmRequest

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'


class ManagerDecisionSchema(BaseModel):
    decision: str = Field(description="Manager decision. Can be one of: accepted or rejected")
    decision_justification: str = Field(description="Justification for manager decision. Optional")


manager = LlmAgent(
    model = MODEL,
    name="manager",
    instruction="""You are sales manager. Your responsibility is to review cases escalated from sales assistants. 
    Review conversation and make decision whether request is approved.
    Decision can ONLY be one of values: "accepted", "rejected"
    If request is rejected provide justification to assistant that can be shared with customer. 
    You can not recommend acceptable discount levels. 
    """,
    description = "Sales manager responsible for review of edge cases like requests for large discounts",
    output_schema = ManagerDecisionSchema
)



# --- Define the Callback Function ---
def before_deal_officer_check(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    agent_name = callback_context.agent_name
    print(f"[Callback] Before model call for agent: {agent_name}")

    if callback_context.state["decision"]=="approved":
        print("[Callback] Proceeding with LLM call.")
        return None
    else:
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="The deal is not approved thereofre it can not move to deal officer")],
            )
        )

deal_officer = LlmAgent(
    model = MODEL,
    name="deal_officer",
    instruction="""
    If the deal is approved collect all the information from the user like payment method and delivery address. 
    Summarize collected information and ask for final approval. 
    If deal is not approved inform the customer that we will then close this session or transfer discussion to assistant if there is anything else we can help with. 
    """,
    description = "Sales manager responsible for review of edge cases like requests for large discounts",
    before_model_callback = before_deal_officer_check
)


manager_as_tool = agent_tool.AgentTool(agent=manager)

async def init_deal_state(callback_context: CallbackContext):
    callback_context.state["deal_state"] = ""
    return None

async def update_deal_state(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
   
    print(f"[Callback] Original tool_response: {tool_response}")
    print(f"[Callback] Tool name: {tool.name}")
    if tool.name  == "manager":
        original_result_value = tool_response
        ##update state
        tool_context.state["decision"] =  original_result_value["decision"]
        ##return original tool response
    return None


assistant = LlmAgent(
    model = MODEL,
    name="assistant",
    instruction="""You are sales assistant. 
    Here is your catalog of products:
    Name: Pixel 9
    Price: $1200
    Color: Black

    Name: Pixel10
    Price: $1500
    Color: Red
    
    You are allowed to give 5% of discount BUT only if the customer really insists. 
    Every larger discount needs to be escalated to manager. 
    Transfer deal to deal officer only if customer accepted the price within discounts you can offer or you have manager approval for larger discount.
    If you think deal can progress to deal officer set state['deal_state'] to "approved".   
    """,
    description = "Sales assistant agent",
    tools = [manager_as_tool],
    sub_agents = [deal_officer],
    before_agent_callback = init_deal_state,
    after_tool_callback = update_deal_state
)

root_agent = assistant