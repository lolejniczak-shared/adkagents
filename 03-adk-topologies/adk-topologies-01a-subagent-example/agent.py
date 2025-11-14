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
from .prompts import personas, get_persona_prompt

load_dotenv()

MODEL = "gemini-2.5-flash"
AGENT_APP_NAME = 'feature_review'


async def init_state(callback_context: CallbackContext):
    """Initializes the state with default review values."""
    for p in personas["merchantPersonas"]:
        callback_context.state[f"persona_{p['id']}_positive_review"] = "Not available"
        callback_context.state[f"persona_{p['id']}_negative_review"] = "Not available"
    return None


persona_agents = []
all_personas = personas["merchantPersonas"] # Get the list once

# --- Main Loop ---
for p in all_personas:
    persona_id = p['id']

    # Define the two sentiments to process for this persona
    sentiments_to_process = [
        ("positive", p['sentiments']['positive']),
        ("negative", p['sentiments']['negative'])
    ]

    # --- NEW: Loop moved *inside* sentiments loop ---
    # We must build a *unique* "other reviews" list for
    # *each* specific agent.
    
    for sentiment_type, sentiment_data in sentiments_to_process:
        
        # This is the unique key for the *current* agent we are building
        current_output_key = f"persona_{persona_id}_{sentiment_type}_review"

        # 1. Build the "other reviews" prompt string
        # This list will contain all reviews *except* the current_output_key
        other_reviews_lines = []
        
        # Iterate through ALL personas (pp) to gather their reviews
        for pp in all_personas:
            other_id = pp['id']
            other_title = pp['title']
            
            # --- Check the positive counterpart ---
            positive_key = f"persona_{other_id}_positive_review"
            # Only add it if it's NOT the current agent's key
            if positive_key != current_output_key:
                other_reviews_lines.append(
                    f"merchant persona: {other_title}: '{pp['sentiments']['positive']['personaName']}'. Positive mindset.\n"
                    f"review: {{{positive_key}}}"
                )
            
            # --- Check the negative counterpart ---
            negative_key = f"persona_{other_id}_negative_review"
            # Only add it if it's NOT the current agent's key
            if negative_key != current_output_key:
                other_reviews_lines.append(
                    f"merchant persona: {other_title}: '{pp['sentiments']['negative']['personaName']}'. Negative mindset.\n"
                    f"review: {{{negative_key}}}"
                )

        # Join all "other review" sections into a single string
        other_reviews_prompt = "\n\n".join(other_reviews_lines)

        # 2. Format the persona-specific details string
        persona_details = f"""Merchant persona name:
 {p['title']}
 Primary Focus Areas:
 {p['primaryFocusAreas']}
 Description:
 {p['description']}
 
 Persona type:
 {sentiment_data['personaName']}
 
 What's on his mind when doing this review:
 {sentiment_data['internalMonologue']}"""

        # 3. Get the base prompt from your function
        base_prompt = get_persona_prompt(persona_details)
        
        # 4. Construct the full instruction prompt
        full_instruction = f"""{base_prompt}

Your previous answer: 
  {{{current_output_key}}}

Answers from other merchant personas representing different perspectives to consider: 
{other_reviews_prompt}
"""
        
        # 5. Create and append the LlmAgent
        agent = LlmAgent(
            model=MODEL,
            name=f"persona_{persona_id}_{sentiment_type}",
            instruction=full_instruction,
            description=(
                f"This agent represents merchant persona named: {p['title']}. "
                f"You have {sentiment_type} mindset. {p['description']}. "
                f"{sentiment_data['internalMonologue']}"
            ),
            output_key=current_output_key, # Use the key we defined
        )
        
        persona_agents.append(agent)

root_agent = LlmAgent(
    model=MODEL,
    name="coordinator",
    instruction="""You are coordinator delegating answers to specialist reviewers from different merchant personas""",
    description="Agent that is responsible for communication specialist reviewers",
    sub_agents = persona_agents,
    before_agent_callback = init_state
)