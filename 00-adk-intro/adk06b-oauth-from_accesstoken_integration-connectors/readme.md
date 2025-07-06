It may happen that when generating access token google.auth.default() will just reuse existing credential file. 
Chances are you did not specify scoped when running: 
gcloud auth application-default login

So scopes when debugging your access tke may be different from those you ask in you code generating access token!

How to fix it:
gcloud auth application-default revoke
gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive.readonly

Also
set quota project
gcloud auth application-default set-quota-project YOUR_PROJECT_ID