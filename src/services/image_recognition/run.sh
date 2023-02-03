#!/bin/bash

gcloud run deploy detect --image us-central1-docker.pkg.dev/encyclo-flower/us/detect --region us-central1 \
    --allow-unauthenticated