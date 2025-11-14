import os
from dotenv import load_dotenv
from google.auth import default, transport
from google.auth.transport.requests import Request
import requests
import vertexai



load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
MEMOERY_GENERATION_MODEL_NAME="gemini-2.5-flash"
EMBEDDING_MODEL_NAME="text-embedding-005"


client = vertexai.Client(
    project=PROJECT_ID,
    location=REGION,
)

agent_engine = client.agent_engines.create(
        config = {
        "displayName": "agent engine with memory bank",    
        "contextSpec": {
            "memoryBankConfig": {
                "generationConfig": {
                    "model": f"projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MEMOERY_GENERATION_MODEL_NAME}"
                },
                "similaritySearchConfig": {
                    "embeddingModel": f"projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{EMBEDDING_MODEL_NAME}"
                }
            }
        }
        }
)

agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
print(agent_engine_id)