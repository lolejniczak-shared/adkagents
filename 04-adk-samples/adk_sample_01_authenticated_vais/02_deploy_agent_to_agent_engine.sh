if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi

adk deploy agent_engine \
--project=${GOOGLE_CLOUD_PROJECT} \
--region=${GOOGLE_CLOUD_LOCATION} \
--staging_bucket=gs://${STAGING_BUCKET} \
--display_name=${AGENTSPACE_ADK_APP_NAME} \
--trace_to_cloud \
agent