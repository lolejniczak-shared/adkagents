import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.openapi_tool.openapi_spec_parser import rest_api_tool, OperationEndpoint
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
import requests
from google import auth as google_auth
from google.auth.transport import requests as google_requests
import uuid
import jwt
load_dotenv()

### Using Integration Connector connectors with authentication  

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'gdrive_manager_with_auth'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
PROJECT_ID=os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION=os.environ["GOOGLE_CLOUD_LOCATION"]
APPLICATION_INTEGRATION_LOCATION = "europe-central2"



auth_credential = None

def get_auth_token() -> str:
    """
    Gets a Google-signed OAuth 2.0 access token for authentication.
    """
    print("Getting authentication token...")
    try:
        # Get the default credentials from the environment (from 'gcloud auth')
        credentials, _ = google_auth.default(
            scopes=[
                "https://www.googleapis.com/auth/drive.readonly",
                "https://www.googleapis.com/auth/drive.metadata",
            ],
            quota_project_id = PROJECT_ID ##OR gcloud auth application-default set-quota-project YOUR_PROJECT_ID
        )
        # Refresh the credentials to get a valid token
        auth_request = google_requests.Request()
        credentials.refresh(auth_request)
        print("Successfully obtained auth token.")
        access_token = credentials.token
        # 2. Use the tokeninfo endpoint to get token details
        tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        response = requests.get(tokeninfo_url, params={'access_token': access_token})
        
        if response.status_code == 200:
            token_info = response.json()
            print("\n--- Token Information ---")
            
            # 'email' or 'sub' (subject) usually identifies the user/service account
            user = token_info.get('email') or token_info.get('sub')
            print(f"👤 Token issued to: {user}")
            
            # 'scope' contains the permissions
            scopes = token_info.get('scope')
            print(f"✅ Permitted Scopes: {scopes}")
            
            # 'aud' (audience) shows which service the token is for
            audience = token_info.get('aud')
            print(f"🎯 Audience (Client ID): {audience}")

        else:
            print(f"\nError inspecting token: {response.status_code} - {response.text}")

        return access_token
    except Exception as e:
        print(f"FATAL: Could not get Google credentials. "
              f"Please run 'gcloud auth application-default login'. Error: {e}")
        raise

existing_access_token = get_auth_token() 

##--------------------------------------------------------------------------------------

if existing_access_token:
        # If an access token is provided, use it directly
        print("Using provided access token for authentication.")
        auth_credential =  AuthCredential(
            auth_type=AuthCredentialTypes.OAUTH2,
            oauth2=OAuth2Auth(
                access_token=existing_access_token  # Set the existing access token
            )
        )
else:
        # Otherwise, own the flow
        print("No access token provided. Configuring for new OAuth2 flow.")
        auth_credential = AuthCredential(
            auth_type=AuthCredentialTypes.OAUTH2,
            oauth2=OAuth2Auth(
                client_id=GOOGLE_CLIENT_ID, 
                client_secret=GOOGLE_CLIENT_SECRET
            ),
        )

auth_scheme = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
            tokenUrl="https://oauth2.googleapis.com/token",
            scopes={
                "openid": "openid",
                "https://www.googleapis.com/auth/drive.readonly": "readonly",
                "https://www.googleapis.com/auth/drive.metadata": "metadata readonly",
                ##"https://www.googleapis.com/auth/cloud-platform": "cloud platform"
            },
        )
    )
)


gdrive_connection_toolset = ApplicationIntegrationToolset(
            project=PROJECT_ID, 
            location=APPLICATION_INTEGRATION_LOCATION, 
            connection="gdrive-connector-with-auth", 
            entity_operations={},
            actions=["GET_files"], 
            ##service_account_credentials='{...}', # optional
            tool_name_prefix="mygdrive",
            tool_instructions="Use this tool to work with gdrive",
            auth_credential=auth_credential,
            auth_scheme=auth_scheme
 )

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant answering all kinds of questions in a very positive way!",
        instruction="If they ask you how you were created, tell them you were created with the Google Agent Framework.",
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
        tools = [gdrive_connection_toolset],
)