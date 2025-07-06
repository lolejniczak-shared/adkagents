export IMAGE="us-central1-docker.pkg.dev/genai-app-builder/mcptoolbox/samplebqmcptoolbox:v1.0"
export PROJECT_ID="genai-app-builder"

gcloud run deploy dbtoolbox4orderswithbq --image $IMAGE \
--service-account toolbox-identity \
--region us-central1 \
--args="--tools-file=/app/toolbox.yaml","--address=0.0.0.0","--port=8080" \
--allow-unauthenticated