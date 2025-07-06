from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os
import json
import os
from dotenv import load_dotenv
import textwrap

load_dotenv()

# New variables for the Object Table
GCS_BUCKET_NAME = f"gs://{os.getenv('STAGING_BUCKET_4_OBJECT_TABLE')}"
PROJECT_ID=os.getenv('BIGQUERY_PROJECT_ID')
LOCATION = os.getenv('BIGQUERY_LOCATION')
BIGQUERY_DATASET_ID = os.getenv('BIGQUERY_DATASET_ID')
BIGQUERY_CONNECTION_NAME  = os.getenv('BIGQUERY_CONNECTION_NAME')
BIGQUERY_OBJECT_TABLE_ID = os.getenv('BIGQUERY_OBJECT_TABLE_ID')
BIGUERY_OUTPUT_TABLE_ID = os.getenv('BIGUERY_OUTPUT_TABLE_ID')
BIGQUERY_REMOTE_FUNCTION_NAME = os.getenv('BIGQUERY_REMOTE_FUNCTION_NAME')
CLOUD_RUN_ENDPOINT = os.getenv('EXECUTOR_CLOUD_RUN_URL')
AGENT_ENGINE_ID=os.getenv('REASONING_ENGINE_ID')

def main():
    """
    Main function to create and use the BigQuery remote function.
    """
    try:
        # 1. Initialize the BigQuery client
        client = bigquery.Client(project=PROJECT_ID)
        print("BigQuery client initialized.")

        # 2. Create the BigQuery Dataset if it doesn't exist
        # This step ensures the script is idempotent.
        print(f"\nAttempting to create or verify dataset `{BIGQUERY_DATASET_ID}`...")
        dataset_id_full = f"{PROJECT_ID}.{BIGQUERY_DATASET_ID}"
        dataset = bigquery.Dataset(dataset_id_full)
        # Datasets are regional resources, so specifying a location is important.
        dataset.location = LOCATION
        # Use exists_ok=True to avoid an error if the dataset already exists.
        client.create_dataset(dataset, exists_ok=True)
        print(f"Successfully ensured dataset `{dataset_id_full}` exists in location `{LOCATION}`.")

        # 2. Define and run the CREATE EXTERNAL TABLE query (DDL for Object Table)
        # This table will list the files in your GCS bucket.
        create_object_table_ddl = textwrap.dedent(f"""
        CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_OBJECT_TABLE_ID}`
        WITH CONNECTION `{PROJECT_ID}.{LOCATION}.{BIGQUERY_CONNECTION_NAME}`
        OPTIONS (
          object_metadata = 'SIMPLE',
          uris = ['{GCS_BUCKET_NAME}/*']
        );
        """)

        print(create_object_table_ddl)
        print("Attempting to create or replace the object table...")
        object_table_job = client.query(create_object_table_ddl)
        object_table_job.result() # Waits for the job to complete
        print(f"Successfully created or replaced object table `{BIGQUERY_OBJECT_TABLE_ID}`.")


        # 3. Define and run the CREATE FUNCTION query (DDL for Remote Function)

        create_function_ddl = textwrap.dedent(f'''
        CREATE OR REPLACE FUNCTION `{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_REMOTE_FUNCTION_NAME}`(
            image_gcs_uri STRING,
            image_content_type STRING,
            text_prompt STRING
        )
        RETURNS STRING LANGUAGE python 
        WITH CONNECTION `{PROJECT_ID}.{LOCATION}.{BIGQUERY_CONNECTION_NAME}`
        OPTIONS (
            entry_point='call_agent_engine_func',
            runtime_version='python-3.11',
            packages=['google-cloud-aiplatform[adk,agent_engines]==1.96', 'google-adk==1.3.0']
        )
        AS r"""
        import json 
        import os 
        from vertexai import agent_engines 

        # The AGENT_ENGINE_RESOURCE_NAME is now directly inserted as a string literal 
        # by the outer f-string, avoiding nested f-string issues. 
        AGENT_ENGINE_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}" 

        def call_agent_engine_func(image_gcs_uri: str, image_content_type: str, text_prompt: str) -> str: 
            try: 
                # Retrieve the remote agent application instance 
                remote_app = agent_engines.get(AGENT_ENGINE_RESOURCE_NAME) 

                # A user_id is required for sessions. You can use a static ID for 
                # this remote function, or make it an input parameter if 
                # you need distinct user identities per call. 
                user_id = "bq_remote_agent_caller" 

                # Create a new session for the interaction with the agent engine 
                remote_session = remote_app.create_session(user_id=user_id) 

                # Construct the message payload, including the image data and text prompt 
                image_message = {{ 
                    "role": "user", 
                    "parts": [ 
                        {{ 
                            "file_data": {{ 
                                "file_uri": image_gcs_uri, 
                                "mime_type": image_content_type,  
                            }}, 
                        }}, 
                        {{ 
                            "text": text_prompt, 
                        }}, 
                    ] 
                }} 

                final_response_text = None 
                # Stream the query to the agent engine and iterate through events 
                for event in remote_app.stream_query( 
                    user_id=user_id, 
                    session_id=remote_session["id"], 
                    message=image_message, 
                ): 
                    # The 'content' field in the event contains the agent's response. 
                    # We assume the relevant response is in the first part and is text. 
                    if "content" in event and "parts" in event["content"] and event["content"]["parts"]: 
                        final_response_text = event["content"]["parts"][0]["text"] 

                if final_response_text: 
                    # Return the agent's response as a JSON string. 
                    # The original Python code expected a JSON response from the agent, 
                    # so we return it directly as a string. 
                    return final_response_text 
                else: 
                    # Handle cases where no valid text response was received 
                    return json.dumps({{"error": "No valid text response received from Agent Engine."}}) 

            except Exception as e: 
                # Catch any exceptions during the process and return an error message 
                return json.dumps({{"error": f"An error occurred while calling the Agent Engine: {{str(e)}}"}}) 
        """
        ''')
        print(create_function_ddl)
        print("\nAttempting to create or replace the remote function...")
        ddl_job = client.query(create_function_ddl)
        ddl_job.result()  # Waits for the job to complete.
        print(f"Successfully created or replaced function `{BIGQUERY_REMOTE_FUNCTION_NAME}`.")
    except NotFound as e:
        print(f"Error: A specified resource was not found. Please check your configuration. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # For query jobs, you can inspect errors more deeply
        if 'query_job' in locals() and hasattr(query_job, 'errors') and query_job.errors:
            print("Query errors:")
            for error in query_job.errors:
                print(f"  - {error['message']}")

if __name__ == "__main__":
    main()