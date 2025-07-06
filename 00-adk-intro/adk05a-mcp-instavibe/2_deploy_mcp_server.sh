#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi


export IMAGE_TAG="latest"
export MCP_IMAGE_NAME="mcp-tool-server"
export IMAGE_PATH="${GOOGLE_CLOUD_LOCATION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${REPO_NAME}/${MCP_IMAGE_NAME}:${IMAGE_TAG}"
export SERVICE_NAME="mcp-tool-server"
export INSTAVIBE_BASE_URL=${INSTAVIBE_BASE_URL}

gcloud builds submit . \
  --tag=${IMAGE_PATH} \
  --project=${GOOGLE_CLOUD_PROJECT}

gcloud run deploy ${SERVICE_NAME} \
  --image=${IMAGE_PATH} \
  --platform=managed \
  --region=${GOOGLE_CLOUD_LOCATION} \
  --allow-unauthenticated \
  --set-env-vars="INSTAVIBE_BASE_URL=${INSTAVIBE_BASE_URL}" \
  --set-env-vars="APP_HOST=0.0.0.0" \
  --set-env-vars="APP_PORT=8080" \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE" \
  --set-env-vars="GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION}" \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT}" \
  --project=${GOOGLE_CLOUD_PROJECT} \
  --min-instances=1