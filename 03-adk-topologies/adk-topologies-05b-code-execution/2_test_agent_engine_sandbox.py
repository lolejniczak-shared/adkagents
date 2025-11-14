import os
from dotenv import load_dotenv
import vertexai
from vertexai import types


load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
SANDBOX_ENVIRONMENT=os.getenv('SANDBOX_ENVIRONMENT')


client = vertexai.Client(
    project=PROJECT_ID,
    location=REGION,
)


sandbox = client.agent_engines.sandboxes.get(name=SANDBOX_ENVIRONMENT)
print(sandbox)

sandbox_name = sandbox.name


##test2 --- notice it maintains state
python_code = """print('Hello world')"""
input_data = {"code": python_code}

response = client.agent_engines.sandboxes.execute_code(
    name = sandbox_name,
    input_data = input_data
)

print(response)
