import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from vertexai.agent_engines import AdkApp
from vertexai.agent_engines import ModuleAgent
import asyncio
import vertexai
from agent_remote_mcp.agent import root_agent
from agent_remote_mcp.agent import mcpt
import json

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"


client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION,
    ##staging_bucket=STAGING_BUCKET,
)


app = AdkApp(
    agent=root_agent
)


## from agent object -- serialization issues
"""
  File "/usr/lib/python3.12/copy.py", line 136, in deepcopy
    y = copier(x, memo)
        ^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/copy.py", line 221, in _deepcopy_dict
    y[deepcopy(key, memo)] = deepcopy(value, memo)
                             ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/copy.py", line 151, in deepcopy
    rv = reductor(4)
         ^^^^^^^^^^^
TypeError: cannot pickle 'TextIOWrapper' instances

remote_app = agent_engines.create(
    display_name = "InstaVibe agent with AdkApp",
    description = "This is basic ADK agent that communicates with InstaVive backend",
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform==1.126.1",
        "google-adk==1.18.0"
        ],
)
"""

schemas = app.register_operations()
print(schemas)

import json

def translate_dict_to_schema(input_map):
    """
    Translates a dictionary of {api_mode: [method_names]} into a list of 
    schema objects with placeholder parameters.
    """
    output_list = []

    for api_mode, methods in input_map.items():
        for method_name in methods:
            # Construct the dictionary entry
            entry = {
                "name": method_name,
                "api_mode": api_mode,
            }
            output_list.append(entry)
            
    return output_list

class_methods = translate_dict_to_schema(schemas)

## from source files
##https://docs.cloud.google.com/agent-builder/agent-engine/deploy#from-source-files

remote_app = client.agent_engines.create(
    config={
        "source_packages": ["agent_remote_mcp"],             # Required. A list of local file or directory paths to include in the deployment.
        "entrypoint_module": "agent",         # Required. The fully qualified Python module name containing the agent entrypoint
        "entrypoint_object": "root_agent",         # Required. The name of the callable object within the entrypoint_module that represents the agent application (for example, root_agent)
        "class_methods": class_methods, ##app.register_operations(),                 # Required.
        ##"requirements_file": "requirements.txt",         # Optional. Defaults to requirements.txt at the root directory of the packaged source.
        "display_name": "InstaVibe agent with AdkApp",                   # Optional.
        "description": """
                This is basic ADK agent that communicates with InstaVive backend
        """,                                            # Optional.
        ##"labels": labels,                               # Optional.
        ##"env_vars": env_vars,                           # Optional.
        ##"build_options": build_options,                 # Optional.
        ##"identity_type": identity_type,                 # Optional. np. types.IdentityType.AGENT_IDENTITY,
        ##"service_account": service_account,             # Optional.
        ##"min_instances": min_instances,                 # Optional.
        ##"max_instances": max_instances,                 # Optional.
        ##"resource_limits": resource_limits,             # Optional.
        ##"container_concurrency": container_concurrency, # Optional
        ##"encryption_spec": encryption_spec,             # Optional.
    },
)