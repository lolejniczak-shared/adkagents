from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent, ParallelAgent
from google.adk.events import Event, EventActions
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from pydantic import BaseModel
from pydantic import Field
import json
from .prompts import personas, get_persona_prompt, SUMMARY_PROMPT
import pandas as pd

load_dotenv()

MODEL = "gemini-2.5-flash"
AGENT_APP_NAME = 'feature_review'


no_of_debate_rounds = 3


async def init_state(callback_context: CallbackContext):
    for p in personas["merchantPersonas"]:
        callback_context.state[f"persona_{p['id']}_positive_review"] = "Not available"
        callback_context.state[f"persona_{p['id']}_negative_review"] = "Not available"
  
    return None

# feature_description = "Possibility to remove items from basket"
persona_agents = []

for p in personas["merchantPersonas"]:
    print(p)
    
    p_positive = f"""Merchant persona name: \n {p['title']} \n Primary Focus Areas:\n {p['primaryFocusAreas']} \n Description:\n {p['description']} \n 
        Persona type:\n {p['sentiments']['positive']['personaName']} \n
        What's on his mind when doing this review:\n {p['sentiments']['positive']['internalMonologue']}"""

    p_negative = f"""Merchant persona name: \n {p['title']} \n Primary Focus Areas:\n {p['primaryFocusAreas']} \n Description:\n {p['description']} \n 
        Persona type:\n {p['sentiments']['negative']['personaName']} \n
        What's on his mind when doing this review:\n {p['sentiments']['negative']['internalMonologue']}"""
 
    _full_instruction_positive = get_persona_prompt(p_positive)
    _full_instruction_negative = get_persona_prompt(p_negative)
    _full_instruction_positive += f"""
    Your previous answer: 
      {{persona_{p['id']}_positive_review}}
    """

    _full_instruction_negative += f"""
    Your previous answer: 
            {{persona_{p['id']}_negative_review}}
    """

    _full_instruction_positive+= f"""
    Answers from other merchant personas representing different perspectives to consider: 
       """
    _full_instruction_negative+= f"""
    Answers from other merchant personas representing different perspectives to consider: 
       """
    
    other_reviews = ""
    for pp in personas["merchantPersonas"]:

        if pp['id'] != p['id']:
            other_reviews += f"""
                merchant persona: {pp['title']}: '{pp['sentiments']['positive']['personaName']}'. Positive mindset. 
                review: {{persona_{pp['id']}_positive_review}}
                
                merchant persona: {pp['title']}: '{pp['sentiments']['negative']['personaName']}'. Negative mindset. 
                review: {{persona_{pp['id']}_negative_review}}
            """
        
    _full_instruction_positive += other_reviews
    _full_instruction_negative += other_reviews

    print(_full_instruction_positive)

    pagent_positive = LlmAgent(
        model=MODEL,
        name=f"persona_{p['id']}_positive",
        instruction=_full_instruction_positive,
        description=f"This agent represents merchant persona named: {p['title']}. You have positive mindset. {p['description']}. {p['sentiments']['positive']['internalMonologue']}.",
        output_key = f"persona_{p['id']}_positive_review",
    )
    persona_agents.append(pagent_positive)

    pagent_negative = LlmAgent(
        model=MODEL,
        name=f"persona_{p['id']}_negative",
        instruction=_full_instruction_negative,
        description = f"This agent represents merchant persona named: {p['title']}. You have negative mindset. {p['description']}. {p['sentiments']['negative']['internalMonologue']}",
        output_key = f"persona_{p['id']}_negative_review",
    )
    persona_agents.append(pagent_negative)
    print("---------------------------------------------")

parallel_agent = ParallelAgent(
    name="ParallelAgent",
    description="This agent runs persona agents in parallel.",
    sub_agents=persona_agents,
)

loop_agent = LoopAgent(
    name="DebateLoop",
    max_iterations=no_of_debate_rounds,
    sub_agents=[parallel_agent],
)

personas_output_keys = [
    f"persona_{p['id']}_{positiveness}_review"
    for p in personas["merchantPersonas"]
    for positiveness in ("positive", "negative")
]

personas_outputs = ""
for persona_name in personas_output_keys:
    personas_outputs += f"\n\n* {personas_output_keys}: {{{personas_output_keys}}}"


async def drop_last_debate_statements_and_summary_to_csv(callback_context: CallbackContext):
    pd.DataFrame(
        [{   
            persona_name: callback_context.state[persona_name].replace("\n", " ").replace("\t", " ")
            for persona_name in personas_output_keys + ["summary"]
        }],
    ).to_csv("debate.csv", index=False)


summary_agent = LlmAgent(
    model=MODEL,
    name="SummaryAgent",
    instruction=SUMMARY_PROMPT.format(input=personas_outputs),
    description = "This agent sums up all the debate statements",
    output_key = "summary",
    after_agent_callback=drop_last_debate_statements_and_summary_to_csv,
)

root_agent = SequentialAgent(
    name="DataPipeline",
    sub_agents=[loop_agent, summary_agent],
    before_agent_callback=init_state
)