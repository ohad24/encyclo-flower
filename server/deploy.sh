#!/bin/sh

cd ${HOME}
docker compose pull
docker compose up -d --remove-orphans
