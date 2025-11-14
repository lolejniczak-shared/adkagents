import os
from dotenv import load_dotenv
import vertexai
from vertexai import types


load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')



client = vertexai.Client(
    project=PROJECT_ID,
    location=REGION,
)

agent_engine = client.agent_engines.create()
agent_engine_name = agent_engine.api_resource.name

agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
print(agent_engine_id)

##LANGUAGE_PYTHON and LANGUAGE_JAVASCRIPT are supported. 
##If machine_config is not specified, the default configuration is 2 vCPU and 1.5 GB of RAM. 
##If you specify MACHINE_CONFIG_VCPU4_RAM4GIB, the sandbox has 4 vCPU and 4GB of RAM.


operation = client.agent_engines.sandboxes.create(
    spec={"code_execution_environment": {
        "code_language": "LANGUAGE_PYTHON",
        "machine_config": "MACHINE_CONFIG_VCPU4_RAM4GIB"
    }},
    name=agent_engine_name,
    config=types.CreateAgentEngineSandboxConfig(display_name="sandbox_4_code_execution")
)

sandbox_name = operation.response.name
print(sandbox_name)


##test2 --- notice it maintains state
python_code = """
            print("Hello world")
"""
input_data = {"code": python_code}

response = client.agent_engines.sandboxes.execute_code(
    name = sandbox_name,
    input_data = input_data
)

print(response)
