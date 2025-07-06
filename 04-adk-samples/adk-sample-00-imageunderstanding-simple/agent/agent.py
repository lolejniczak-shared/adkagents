from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, LoopAgent
from pydantic import BaseModel
from pydantic import Field
from google.adk.examples import Example
from google.adk.tools import ExampleTool

load_dotenv()

MODEL = "gemini-2.5-flash"
AGENT_APP_NAME = 'tree_doctor'

doctor_instruction="""
    You are an experienced arborist specializing in Thuja (arborvitae) trees. Your task is to visually assess the health of a Thuja tree based on an image provided by the user.

    When evaluating the image, please carefully examine the following aspects:

    Overall Color: Is the foliage a vibrant green, or are there signs of yellowing, browning, or discoloration? Note any specific patterns of discoloration (e.g., tips, patches, entire branches).
    Foliage Density: Does the tree appear full and dense, or are there sparse areas, bare patches, or visible gaps between branches?
    Branch Integrity: Are the branches firm and upright, or do they appear droopy, brittle, or broken? Look for any signs of dieback or wilting.
    Presence of Pests/Diseases: Look for any visible signs of pests (e.g., webbing, sticky residue, small insects, holes in foliage) or diseases (e.g., fungal spots, powdery mildew, cankers, unusual growths).
    Trunk and Base: Examine the base of the tree and the visible parts of the trunk for any lesions, cracks, peeling bark, or signs of rot.
    Overall Vigor: Does the tree appear healthy and thriving, or stressed and struggling?
    After your assessment, please provide a concise evaluation of the tree's health using one of the following categories:

    Healthy: The tree appears to be in excellent condition with no visible signs of stress, disease, or pests.
    Requires Closer Attention: The tree shows some minor signs of stress or early symptoms of a potential issue (e.g., slight discoloration, minor thinning). Further investigation or basic care might be needed.
    Unhealthy/Diseased: The tree exhibits significant signs of stress, widespread discoloration, severe thinning, or clear evidence of disease or pest infestation. Immediate and targeted intervention is likely required
    """

number_of_doctors = 3
doctors = []
for i in range(number_of_doctors):

    doctor = LlmAgent(name=f"doctor{i}", 
    model = MODEL, 
    instruction=doctor_instruction, 
    output_key=f"audit_result_{i}",
    )


    
    doctors.append(doctor)

doctor_assessments = ParallelAgent(
    name="ParallelAssesment",
    sub_agents=doctors
)

aggregator = LlmAgent(
    model = MODEL,
    name="Synthesizer",
    instruction="""Combine assessments from all doctors. 
    Make final decision selecting one of the options: 
    Healthy: The tree appears to be in excellent condition with no visible signs of stress, disease, or pests.
    Requires Closer Attention: The tree shows some minor signs of stress or early symptoms of a potential issue (e.g., slight discoloration, minor thinning). Further investigation or basic care might be needed.
    Unhealthy/Diseased: The tree exhibits significant signs of stress, widespread discoloration, severe thinning, or clear evidence of disease or pest infestation. Immediate and targeted intervention is likely required
    Generate detailed description how and why you made this final choice. 
    """
)

class OutputSchema(BaseModel):
    status: str = Field(description="The decision about tree health status")
    summary: str = Field(description="The description of tree health status")

structure_answer = Agent(
    model=MODEL,
    name="stucture",
    instruction="""Structure final answer as JSON""",
    description="""You are agent responsible for structuring the final answer""",
    ##input_schema=InputSchema,
    output_schema=OutputSchema,
)

root_agent = SequentialAgent(
    name="main",
    sub_agents=[doctor_assessments, aggregator, structure_answer] # Run parallel fetch, then synthesize
)