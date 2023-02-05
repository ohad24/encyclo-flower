#!/bin/bash


#gcloud builds submit \
#    --tag us-central1-docker.pkg.dev/encyclo-flower/us/detect

# gcloud builds submit --config=cloudbuild.yaml --substitutions=AAA="aaa"

export _AAA="aaa123"
# gcloud builds submit --config=cloudbuild.yaml --substitutions=_AAA=$_AAA
gcloud builds submit --config=cloudbuild.yaml
    