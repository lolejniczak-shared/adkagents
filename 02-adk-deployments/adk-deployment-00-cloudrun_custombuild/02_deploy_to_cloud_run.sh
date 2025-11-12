export IMAGE=gcr.io/genai-app-builder/customadkimage

gcloud run deploy customadkdeployment \
 --image $IMAGE \
 --service-account toolbox-identity \
 --region us-central1 \
 --allow-unauthenticated