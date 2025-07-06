export IMAGE=gcr.io/genai-app-builder/customadkimage
gcloud builds submit --tag $IMAGE .
