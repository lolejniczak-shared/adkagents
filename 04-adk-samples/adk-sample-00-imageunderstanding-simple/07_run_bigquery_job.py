from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os
import json
import os
from dotenv import load_dotenv

load_dotenv()

load_dotenv()

PROJECT_ID=os.getenv('BIGQUERY_PROJECT_ID')
LOCATION = os.getenv('BIGQUERY_LOCATION')
BIGQUERY_DATASET_ID = os.getenv('BIGQUERY_DATASET_ID')
BIGQUERY_OBJECT_TABLE_ID = os.getenv('BIGQUERY_OBJECT_TABLE_ID')
BIGQUERY_OUTPUT_TABLE_ID = os.getenv('BIGQUERY_OUTPUT_TABLE_ID')
BIGQUERY_REMOTE_FUNCTION_NAME = os.getenv('BIGQUERY_REMOTE_FUNCTION_NAME')


def main():
        # 1. Initialize the BigQuery client
        client = bigquery.Client(project=PROJECT_ID)
        print("BigQuery client initialized.")
        select_query = f"""
        CREATE OR REPLACE TABLE `{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_OUTPUT_TABLE_ID}` AS
        WITH
          audits AS (
            SELECT
              uri AS gcs_uri, -- The column from the object table is named 'uri'
              content_type,
              `{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_REMOTE_FUNCTION_NAME}`(uri, content_type, "what is the state of this tree?") AS audit_results
            FROM
              `{PROJECT_ID}.{BIGQUERY_DATASET_ID}.{BIGQUERY_OBJECT_TABLE_ID}`
           )
        SELECT
          gcs_uri,
          JSON_VALUE(audit_results, '$.summary') AS summary,
          JSON_VALUE(audit_results, '$.status') AS coverage
        FROM
          audits
        """
        print("\nRunning query to audit images...")
        print(select_query)
        print("============================")
        query_job = client.query(select_query) 
        print("Waiting for query job to finish...")
        query_job.result() 
        print("Query finished. Table created successfully.")

if __name__ == "__main__":
    main()