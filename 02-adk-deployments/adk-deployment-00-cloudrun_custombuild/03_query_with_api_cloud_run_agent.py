import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
import json
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import uuid
import requests
from google.oauth2 import id_token
import json

load_dotenv()

# 1. --- Configuration ---
# Load environment variables from your .env file
load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
AGENT_CLOUD_RUN_URL = os.getenv('AGENT_CLOUD_RUN_URL')
ADK_APP_NAME = os.getenv('ADK_APP_NAME')

# The specific GCS image you want to send for the audit
# Using the image from your original example
GCS_IMAGE_URI = "gs://zabka-pieczywo/audyt_pieczywo3.jpg"

def get_auth_token() -> str:
    """
    Gets a Google-signed OAuth 2.0 access token for authentication.
    """
    print("Getting authentication token...")
    try:
        auth_req = google_auth.transport.requests.Request()
        tid_token = id_token.fetch_id_token(auth_req, AGENT_CLOUD_RUN_URL)
        return tid_token
    except Exception as e:
        print(f"FATAL: Could not get Google credentials. "
              f"Please run 'gcloud auth application-default login'. Error: {e}")
        raise



# 2. --- Main Execution ---
if __name__ == "__main__":
    if not all([PROJECT_ID, LOCATION, AGENT_CLOUD_RUN_URL]):
        print("FATAL: One or more required environment variables are not set.")
        exit(1)

    try:
        # Get the required token to authorize our API call
        token = get_auth_token()

        # 3. --- Construct the API Request ---
        # The full REST endpoint for a direct, non-streaming query
        url = AGENT_CLOUD_RUN_URL+"/run_sse"

        # The headers, including our authorization token
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        message = {
                "role": "user",
                "parts": [
                    {
                    "fileData": {
                        "mimeType": "image/jpg",
                        "fileUri": GCS_IMAGE_URI
                    }
                    },
                    {
                        "text": "What is the stock level of breadstuff on this image?"
                    }
                ]
            }
    
        id = str(uuid.uuid4())
        user_id = f"test-user-{id}"

        ## create session:
        app_name = ADK_APP_NAME
        new_session_url = AGENT_CLOUD_RUN_URL+"/apps"+"/"+app_name+"/users/"+user_id+"/sessions/"+id
        state = { "state": {} }
        session_name = id
        response = requests.post(new_session_url, headers=headers, json=state)
        ##session_id = get_session_from_operation(response)


        ## https://adkhelloworld-680248386202.us-central1.run.app/list-apps to see if you have consistent app name
        payload =  {
            "app_name": app_name,
            "user_id": user_id,
            "session_id": id,
            "new_message": message,
            "streaming": True
        }
        
        print("With payload:")
        print(json.dumps(payload, indent=2))

        # 4. --- Send the Request and Process the Response ---
        event_data = None
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status() # Check for HTTP errors
            
            # Use iter_lines to process each line of the SSE stream as it arrives
            for line in response.iter_lines():
                if line: # Filter out keep-alive new lines
                    decoded_line = line.decode('utf-8')
                    
                    # SSE events are prefixed with "data: ". We check for that prefix.
                    if decoded_line.startswith('data:'):
                        # Remove the "data: " prefix to get the JSON content
                        event_data_str = decoded_line[len('data:'):].strip()
                        
                        try:
                            # Parse the JSON string into a Python dictionary
                            event_data = json.loads(event_data_str)
                        except json.JSONDecodeError:
                            # Handle cases where the data part is not valid JSON
                            print(f"--- WARNING: Received non-JSON data: {event_data_str} ---")

        print(event_data)
    except Exception as e:
        # Handle other errors (e.g., network issues, authentication failure)
        print(f"\n--- ERROR: An unexpected error occurred ---")
        print(e)