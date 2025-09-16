import json
import os
from dotenv import load_dotenv

import json
from typing import List

import requests
from google.api_core.exceptions import NotFound
from google.cloud import storage
import google.cloud.discoveryengine_v1 as discoveryengine
from google.auth import transport
import google.auth
from google.auth import default

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("DATASTORE_LOCATION")
DATA_STORE_ID = os.getenv("DATASTORE_ID")
BRANCH_ID = "0"

def list_indexed_documents(
    project_id: str,
    location: str,
    data_store_id: str
  ):

            client_options = (
                ClientOptions(api_endpoint=f"{location}-discoveryengine.googleapis.com")
                if location != "global"
                else None
            )

            # Create a client
            client = discoveryengine.DocumentServiceClient(client_options=client_options)

            # The full resource name of the search engine branch.
            # e.g. projects/{project}/locations/{location}/dataStores/{data_store}/branches/{branch}
            parent = client.branch_path(
                project=project_id,
                location=location,
                data_store=data_store_id,
                branch="default_branch",
            )

            response = client.list_documents(parent=parent)
            ##print(response)
            for document in response.documents:
                    print(document)
                    print("************")

##ListDocuments is not available for an acled datastore.



class DatastoreService:
    def __init__(self):
        creds, project_id = default()
        auth_req = transport.requests.Request()  # Use google.auth here
        creds.refresh(auth_req)
        access_token = creds.token
        self.access_token = access_token


    def search_datastore(self, project_id, location, datastore_id, query):
        # Define API endpoint and headers
        url = f"https://{location}-discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{datastore_id}/servingConfigs/default_search:search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Define request data with placeholders for query
        ##https://cloud.google.com/generative-ai-app-builder/docs/reference/rest/v1beta/projects.locations.collections.dataStores.servingConfigs/search
        data = {
            "query": f"{query}",
            "pageSize":10,
            "queryExpansionSpec":{"condition":"AUTO"},
            "spellCorrectionSpec":{"mode":"AUTO"},
            "relevanceScoreSpec":{"returnRelevanceScore":True},
            "languageCode":"en-US",
            "contentSearchSpec":{"snippetSpec":{"returnSnippet":True}},
            "naturalLanguageQueryUnderstandingSpec":{"filterExtractionCondition":"ENABLED"},
            "userInfo":{"timeZone":"Europe/Warsaw"}
            }

        # Make POST request
        response = requests.post(url, headers=headers, json=data)
        resp = response.json()
        print(resp)
        return resp

##list_indexed_documents(PROJECT_ID, LOCATION, DATA_STORE_ID)

query_for_bard = "Q3 Sales Performance Report" ##should not find anything here
query_for_admin = "Employee Handbook" ##should find something here

service = DatastoreService()
print("Expected  empty result set")
service.search_datastore(PROJECT_ID, LOCATION, DATA_STORE_ID, query_for_bard)

print("Expected  TSK-1003")
service.search_datastore(PROJECT_ID, LOCATION, DATA_STORE_ID, query_for_admin)

