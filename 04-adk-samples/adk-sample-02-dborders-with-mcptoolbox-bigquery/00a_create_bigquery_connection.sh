#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi


# Set environment variables for convenience
export REGION=${GOOGLE_CLOUD_LOCATION}
export PROJECT_ID=${GOOGLE_CLOUD_PROJECT}
export REASONING_ENGINE_ID=${REASONING_ENGINE_ID}


# --- 1. Check for Existing Connection ---
echo "Checking if connection '${BIGQUERY_CONNECTION_NAME}' already exists in project '${PROJECT_ID}' and region '${REGION}'..."

# Use `bq show` to check for the connection.
# We redirect stdout and stderr to /dev/null because we only care about the exit code.
# A non-zero exit code means the connection was not found.
bq show --connection \
    --project_id=${PROJECT_ID} \
    --location=${REGION} \
    ${BIGQUERY_CONNECTION_NAME} > /dev/null 2>&1

# --- 2. Create Connection if it Doesn't Exist ---
# Check the exit code of the `bq show` command.
if [ $? -ne 0 ]; then
  echo "Connection not found. Proceeding with creation..."

  # The `bq mk` command to create the connection.
  bq mk --connection \
      --connection_type=CLOUD_RESOURCE \
      --project_id=${PROJECT_ID} \
      --location=${REGION} \
      --display_name="Connection for ${BIGQUERY_CONNECTION_NAME}" \
      ${BIGQUERY_CONNECTION_NAME}

  # Check the exit code of the bq mk command to confirm success.
  if [ $? -eq 0 ]; then
    echo "Connection '${BIGQUERY_CONNECTION_NAME}' created successfully."
  else
    # If creation fails, print an error and exit.
    echo "Error: Failed to create connection '${BIGQUERY_CONNECTION_NAME}'. Please check the output above."
    exit 1
  fi
else
  # If the `bq show` command succeeded, the connection already exists.
  echo "Connection '${BIGQUERY_CONNECTION_NAME}' already exists. Skipping creation."
fi


# --- Get Service Account (This should now succeed) ---
echo "Retrieving service account for connection '${BIGQUERY_CONNECTION_NAME}'..."
CONNECTION_SA=$(bq show --connection --project_id=${PROJECT_ID} --location=${REGION} --format=json ${BIGQUERY_CONNECTION_NAME} | jq -r '.cloudResource.serviceAccountId')

if [ -z "${CONNECTION_SA}" ]; then
  echo "FATAL ERROR: Failed to retrieve the service account for the BigQuery connection."
  echo "How to debug:"
  echo "1. Check if the connection exists in the Google Cloud Console."
  echo "2. Run the command below manually to see the exact error message:"
  echo "   bq show --connection --project_id=${PROJECT_ID} --location=${REGION} ${BIGQUERY_CONNECTION_NAME}"
  exit 1
fi

echo "Successfully retrieved BigQuery Connection Service Account: ${CONNECTION_SA}"

## Grant invoker role to Cloud Run so that it is able to run executor deployd in step 4
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${CONNECTION_SA}" \
    --role="roles/aiplatform.user" \
    --condition=None
