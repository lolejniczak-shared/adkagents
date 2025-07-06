gcloud auth application-default login --impersonate-service-account=680248386202-compute@developer.gserviceaccount.com

gcloud config set auth/impersonate_service_account 680248386202-compute@developer.gserviceaccount.com
gcloud auth list
gcloud config unset auth/impersonate_service_account