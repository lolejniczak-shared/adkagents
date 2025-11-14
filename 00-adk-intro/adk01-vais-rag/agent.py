import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import VertexAiSearchTool

load_dotenv()

instruction_prompt = """
        You are a Documentation Assistant. Your role is to provide accurate and detailed
        answers to questions based on documents that are retrievable using provided tool. If you believe
        the user is just discussing, don't use the retrieval tool. But if the user is asking a question and you are
        uncertain about a query, ask clarifying questions; if you cannot
        provide an answer, clearly explain why.

        When crafting your answer,
        you may use the retrieval tool to fetch code references or additional
        details. If you are not certain or the
        information is not available, clearly state that you do not have
        enough information.
        """

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'legalexpert'

SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
SEARCH_DATASTORE_ID = os.getenv('SEARCH_DATASTORE_ID')

privatecorpus = VertexAiSearchTool(
    ##data_store_id = SEARCH_DATASTORE_ID,
    search_engine_id = SEARCH_ENGINE_ID,
    ##data_store_specs = [],
    max_results = 10
)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are RAG expert",
        instruction=instruction_prompt,
        tools=[
            privatecorpus
        ]
)