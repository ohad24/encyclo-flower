#!/bin/sh

git clone git@github.com:ohad24/encyclo-flower.git
cd encyclo-flower
python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install --upgrade -r src/api/requirements.txt
export MONGO_DB_NAME="dev"
export MONGO_URI="mongodb://root:example@localhost:27017"
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/src/api/google_cred.json
docker compose -f src/db/docker-compose.yml up -d
