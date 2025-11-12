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
from agent_engine_config import _AGENT_ENGINE_CLASS_METHODS 

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

"""
schemas = app.register_operations()
print(schemas)

import json

def translate_dict_to_schema(input_map):
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
"""

class_methods = _AGENT_ENGINE_CLASS_METHODS ##translate_dict_to_schema(schemas)

## from source files
##https://docs.cloud.google.com/agent-builder/agent-engine/deploy#from-source-files

remote_app = client.agent_engines.create(
    config={
        "source_packages": ["agent_remote_mcp/","agent_engine_app.py"],             # Required. A list of local file or directory paths to include in the deployment.
        "entrypoint_module": "agent_engine_app",         # Required. The fully qualified Python module name containing the agent entrypoint
        "entrypoint_object": "adkapp",         # Required. The name of the callable object within the entrypoint_module that represents the agent application (for example, root_agent)
        "class_methods": class_methods, ##app.register_operations(),                 # Required.
        "requirements_file": "./agent_remote_mcp/requirements.txt",         # Optional. Defaults to requirements.txt at the root directory of the packaged source.
        "display_name": "InstaVibe from source files",                   # Optional.
        "description": """
                This is basic ADK agent that communicates with InstaVive backend
        """,                                            # Optional.
        ##"labels": labels,                               # Optional.
        "env_vars": {
            ##"GOOGLE_CLOUD_PROJECT": "genai-app-builder", {'error': {'code': 400, 'message': "Environment variable name 'GOOGLE_CLOUD_PROJECT' is reserved.
            ##"GOOGLE_GENAI_USE_VERTEXAI": "1",
            ##"GOOGLE_CLOUD_LOCATION": "us-central1",
            "MCP_SERVER_URL": "https://mcp-tool-server-680248386202.us-central1.run.app"
        },                           # Optional.
        ##"build_options": build_options,                 # Optional.
        ##"identity_type": identity_type,                 # Optional. np. types.IdentityType.AGENT_IDENTITY,
        ##"service_account": service_account,             # Optional.
        ##"min_instances": min_instances,                 # Optional.
        ##"max_instances": max_instances,                 # Optional.
        ##"resource_limits": resource_limits,             # Optional.
        ##"container_concurrency": container_concurrency, # Optional
        ##"encryption_spec": encryption_spec,             # Optional.
        "agent_framework": 'google-adk'
    },
)