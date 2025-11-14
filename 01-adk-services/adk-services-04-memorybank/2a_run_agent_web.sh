# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi

adk web --memory_service_uri "${AGENT_ENGINE_RESOURCE_NAME}" --log_level debug