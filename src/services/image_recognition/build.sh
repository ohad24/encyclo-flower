#!/bin/bash


gcloud builds submit \
    --tag us-central1-docker.pkg.dev/encyclo-flower/us/detect
    