# dashclusters
A simple dashboard demo for clustering

## Build docker image and run
`docker build -t simpledashboard:latest .`  
`docker run -it simpledashboard:latest`

## Build and Deploy to Google Cloud Run
`gcloud builds submit --tag gcr.io/{ProjectID}/dash-clusters  --project={ProjectID}`
`gcloud run deploy --image gcr.io/{ProjectID}/dash-clusters --platform managed  --project={ProjectID} --allow-unauthenticated`
