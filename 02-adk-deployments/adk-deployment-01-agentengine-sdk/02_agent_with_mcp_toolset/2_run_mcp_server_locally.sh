# Check if .env file exists
if [ -f .env ]; then
  # Export variables from .env file
  export $(grep -v '^#' .env | xargs)
fi

fastmcp run instavibe_mcpserver.py --transport=http --port=8080 --host=0.0.0.0
##host is required for this to work on Cloud Run