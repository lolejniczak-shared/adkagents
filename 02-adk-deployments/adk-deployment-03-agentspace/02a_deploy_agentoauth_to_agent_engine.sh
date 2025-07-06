adk deploy agent_engine \
--project="genai-app-builder" \
--region="us-central1" \
--staging_bucket="gs://lolejniczak-adk-training" \
--trace_to_cloud \
--display_name="grive_oauth_agent" \
--description="Agent using gdrive integration connector as tool with oauth2 enabled" \
agentoauth