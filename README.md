# dashclusters
A simple dashboard demo for clustering

## Build docker image and run
`docker build -t simpledashboard:latest .`  
`docker run -it simpledashboard:latest`

## Deploy to build and deploy to Google Cloud Run
`gcloud builds submit --tag gcr.io/ProjectID/dash-youtube-example  --project=ProjectID`
`gcloud run deploy --image gcr.io/ProjectID/dash-youtube-example --platform managed  --project=ProjectID --allow-unauthenticated`

