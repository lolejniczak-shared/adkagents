import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.google_api_tool import GmailToolset, DocsToolset
from google.adk.planners.plan_re_act_planner  import PlanReActPlanner

load_dotenv()

MODEL = "gemini-2.5-pro"
AGENT_APP_NAME = 'enterpriseagent'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

docs_toolset = DocsToolset(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
gmail_toolset = GmailToolset(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant orchestrating actions on google docs, gmail",
        instruction="You are coordinating actions across google tools like gmail, docs, sheets, slides",
        tools = [gmail_toolset, docs_toolset],
        planner = PlanReActPlanner()
)