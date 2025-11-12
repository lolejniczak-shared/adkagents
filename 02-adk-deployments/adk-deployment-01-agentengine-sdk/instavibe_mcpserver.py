import requests
import json
import os
from dotenv import load_dotenv

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

from urllib.parse import urlparse

from typing import Optional, Dict, Any

from fastmcp import FastMCP
from instavibe import create_event,create_post

mcp = FastMCP("Demo 🚀")

load_dotenv()
BASE_URL = os.environ.get("INSTAVIBE_BASE_URL")

def get_id_token(audience_url: str) -> str | None:
    """
    Fetches a Google-signed ID token for the specified audience.
    Uses Application Default Credentials (ADC).

    Args:
        audience_url (str): The URL of the Cloud Run service (the audience).
                          e.g., "https://my-service-abcde.a.run.app"

    Returns:
        str | None: The fetched ID token, or None if an error occurs.
    """
    print(f"Attempting to fetch ID token for audience: {audience_url}")
    try:
        # Get default credentials
        credentials, project = google.auth.default()

        # Create an authed request object
        auth_request = google.auth.transport.requests.Request()

        # Fetch the ID token
        # The audience is the base URL of the Cloud Run service
        token = google.oauth2.id_token.fetch_id_token(auth_request, audience_url)
        print("Successfully fetched ID token.")
        return token
    except Exception as e:
        print(f"Error fetching ID token: {e}")
        print("Please ensure you have authenticated with 'gcloud auth application-default login'")
        print("or that your service account has the 'Cloud Run Invoker' role.")
        return None


def verify_google_id_token(token_string: str, audience: str) -> Optional[Dict[str, Any]]:
    """
    Parses and verifies a Google-signed ID token.

    Args:
        token_string (str): The encoded ID token string (the JWT).
        audience (str): The expected audience of the token (your Cloud Run URL).

    Returns:
        dict | None: The decoded token payload (claims) if verification is successful.
                     Returns None if verification fails.
    """
    if not audience:
        print("Error: Audience (INSTAVIBE_BASE_URL) is not set. Cannot verify token.")
        return None
        
    if not token_string:
        print("Error: No token string provided.")
        return None

    try:
        # verify_oauth2_token checks all of the following:
        # 1. Token is properly signed by Google.
        # 2. Token is not expired (exp claim).
        # 3. Audience (aud claim) matches your service's URL.
        # 4. Issuer (iss claim) is 'https://accounts.google.com' or 'accounts.google.com'.
        auth_request = google.auth.transport.requests.Request()
        id_info = google.oauth2.id_token.verify_oauth2_token(token_string, auth_request, audience)
        print(id_info)

        print("Token successfully verified.")
        return id_info

    except ValueError as e:
        # This exception is a catch-all for any verification failure:
        # - Invalid signature
        # - Expired token
        # - Wrong audience
        # - Wrong issuer
        # - etc.
        print(f"Error: Token verification failed: {e}")
        return None
    except Exception as e:
        # Catch other potential errors
        print(f"An unexpected error occurred during token verification: {e}")
        return None

@mcp.tool()
def create_post(author_name: str, text: str, sentiment: str, base_url: str = BASE_URL):
    """
    Sends a POST request to the /posts endpoint to create a new post.

    Args:
        author_name (str): The name of the post's author.
        text (str): The content of the post.
        sentiment (str): The sentiment associated with the post (e.g., 'positive', 'negative', 'neutral').
        base_url (str, optional): The base URL of the API. Defaults to BASE_URL.

    Returns:
        dict: The JSON response from the API if the request is successful.
              Returns None if an error occurs.

    Raises:
        requests.exceptions.RequestException: If there's an issue with the network request (e.g., connection error, timeout).
    """
    url = f"{base_url}/posts"
    parsed_url = urlparse(url)
    root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    token = get_id_token(root_url)
    
    if not token:
            print("Aborting post creation due to authentication failure.")
            return None
    verify_google_id_token(token, root_url)
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"  # Add the token as a Bearer token
    }
    payload = {
        "author_name": author_name,
        "text": text,
        "sentiment": sentiment
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"Successfully created post. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating post: {e}")
        # Optionally re-raise the exception if the caller needs to handle it
        # raise e
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

@mcp.tool()
def create_event(event_name: str, description: str, event_date: str, locations: list, attendee_names: list[str], base_url: str = BASE_URL):
    """
    Sends a POST request to the /events endpoint to create a new event registration.

    Args:
        event_name (str): The name of the event.
        description (str): The detailed description of the event.
        event_date (str): The date and time of the event (ISO 8601 format recommended, e.g., "2025-06-10T09:00:00Z").
        locations (list): A list of location dictionaries. Each dictionary should contain:
                          'name' (str), 'description' (str, optional),
                          'latitude' (float), 'longitude' (float),
                          'address' (str, optional).
        attendee_names (list[str]): A list of names of the people attending the event.
        base_url (str, optional): The base URL of the API. Defaults to BASE_URL.

    Returns:
        dict: The JSON response from the API if the request is successful.
              Returns None if an error occurs.

    Raises:
        requests.exceptions.RequestException: If there's an issue with the network request (e.g., connection error, timeout).
    """
    url = f"{base_url}/events"
    token = get_id_token(base_url)
    if not token:
            print("Aborting post creation due to authentication failure.")

    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",  # Add the token as a Bearer token
            "X-Serverless-Authorization": f"Bearer {token}"
    }
    payload = {
        "event_name": event_name,
        "description": description,
        "event_date": event_date,
        "locations": locations,
        "attendee_names": attendee_names,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"Successfully created event registration. Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating event registration: {e}")
        # Optionally re-raise the exception if the caller needs to handle it
        # raise e
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from {url}. Response text: {response.text}")
        return None

if __name__ == "__main__":
    mcp.run() ##transport, port, host specified in 2_run_mcp_server_locally.sh