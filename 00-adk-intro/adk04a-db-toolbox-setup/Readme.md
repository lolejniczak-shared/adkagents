curl -O https://storage.googleapis.com/genai-toolbox/v0.7.0/linux/amd64/toolbox
chmod +x toolbox
./toolbox --tools-file "toolbox.yaml"

##### by default MCP-toolbox imports tools.yaml thorugh secrets we need to therefore create custom iamge


## build cudtom docker image 
cd 



####ERROR "toolbox failed to initialize: unable to initialize source \"alloydb-toys\": unable to connect successfully: failed to connect to `user=toolbox-identity@genai-app-builder.iam database=postgres`: /tmp/.s.PGSQL.5432 (/tmp): failed SASL auth: FATAL: password authentication failed for user \"toolbox-identity@genai-app-builder.iam\" (SQLSTATE 28P01)"


gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:toolbox-identity@genai-app-builder.iam.gserviceaccount.com" \
    --role="roles/alloydb.databaseUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:toolbox-identity@genai-app-builder.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

Also make sure Alloydb flag is set: alloydb.iam_authentication=on 


gcloud alloydb users create toolbox-identity@genai-app-builder.iam \
    --cluster="vector-cluster" \
    --region="us-central1" \
    --type=IAM_BASED

GRANT CONNECT ON DATABASE your_target_database TO "toolbox-identity@genai-app-builder.iam";
GRANT USAGE ON SCHEMA your_target_schema TO "toolbox-identity@genai-app-builder.iam";
GRANT SELECT ON ALL TABLES IN SCHEMA your_target_schema TO "toolbox-identity@genai-app-builder.iam";



export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
export PROJECT_ID="genai-app-builder"

gcloud run deploy dbtoolbox --image $IMAGE --service-account toolbox-identity --region us-central1 --args="--tools-file=/app/tools.yaml","--address=0.0.0.0","--port=8080" --allow-unauthenticated