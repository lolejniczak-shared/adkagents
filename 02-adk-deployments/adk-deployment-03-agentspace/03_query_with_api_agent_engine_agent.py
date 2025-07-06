import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
import json
import requests
from dotenv import load_dotenv

from google import auth as google_auth
from google.auth.transport import requests as google_requests
import uuid

# 1. --- Configuration ---
# Load environment variables from your .env file
load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
REASONING_ENGINE_ID = os.getenv('REASONING_ENGINE_ID_4_AGENTOAUTH')

# The specific GCS image you want to send for the audit
# Using the image from your original example

def get_auth_token() -> str:
    """
    Gets a Google-signed OAuth 2.0 access token for authentication.
    """
    print("Getting authentication token...")
    try:
        # Get the default credentials from the environment (from 'gcloud auth')
        credentials, _ = google_auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform",
                "openid",
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/drive.metadata"]
        )
        # Refresh the credentials to get a valid token
        auth_request = google_requests.Request()
        credentials.refresh(auth_request)
        print("Successfully obtained auth token.")
        return credentials.token
    except Exception as e:
        print(f"FATAL: Could not get Google credentials. "
              f"Please run 'gcloud auth application-default login'. Error: {e}")
        raise

# 2. --- Main Execution ---
if __name__ == "__main__":
    if not all([PROJECT_ID, LOCATION, REASONING_ENGINE_ID]):
        print("FATAL: One or more required environment variables are not set.")
        exit(1)

    try:
        # Get the required token to authorize our API call
        token = get_auth_token()

        # 3. --- Construct the API Request ---
        # The full REST endpoint for a direct, non-streaming query
        url = (
            f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}"
            f"/locations/{LOCATION}/reasoningEngines/{REASONING_ENGINE_ID}:streamQuery?alt=sse"
        )

        # The headers, including our authorization token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        image_message = {
            "role": "user",
            "parts": [
                {
                    "text": "show me my gdrive files",
                },
            ]
        }
        user_id = f"test-user-{uuid.uuid4()}"
        payload = {
             "class_method": "stream_query", # This key is often optional for the default query method
             "input": {
                "user_id": user_id,
                ##"session_id": self.session_id,
                "message": image_message
             }
        }
        
        print(f"\nSending POST request to: {url}")
        print("With payload:")
        print(json.dumps(payload, indent=2))

        # 4. --- Send the Request and Process the Response ---
        event_data = None
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status() # Check for HTTP errors
            
            # Use iter_lines to process each line of the SSE stream as it arrives
            for line in response.iter_lines():
                    decoded_line = line.decode('utf-8')
                    event_data_str = decoded_line.strip() 
                    try:
                            event_data = json.loads(event_data_str)
                    except json.JSONDecodeError:
                            print(f"--- WARNING: Received non-JSON data: {event_data_str} ---")
        print(event_data)
    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors from the API
        print(f"\n--- ERROR: HTTP Error occurred ---")
        print(f"Status Code: {http_err.response.status_code}")
        print("Response Body:")
        # Print the error details from the API if available
        print(http_err.response.text)
    except Exception as e:
        # Handle other errors (e.g., network issues, authentication failure)
        print(f"\n--- ERROR: An unexpected error occurred ---")
        print(e)