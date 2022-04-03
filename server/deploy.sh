#!/bin/sh

gcp_metadata_json_to_env() {
    # This function is used to get metadata from the GCP metadata server and write it to a file
    # The value is expected to be in json format and the output will be a .env file
    # The first parameter is the metadata key to retrieve
    # The second parameter is the file to write the metadata to
    METADATA_URL='http://metadata.google.internal/computeMetadata/v1/project/attributes'
    curl -fsL "${METADATA_URL}/${1}" -H "Metadata-Flavor: Google" | jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" > "${2}"
}

# Ensure .env files are updated before deploying
gcp_metadata_json_to_env "PRODUCTION" "${HOME}/PRODUCTION.env"
gcp_metadata_json_to_env "DEVELOPMENT" "${HOME}/DEVELOPMENT.env"

DOCKER_COMPOSE_YML="${HOME}/docker-compose.yml"
docker compose -f ${DOCKER_COMPOSE_YML} pull
docker compose -f ${DOCKER_COMPOSE_YML} up -d --remove-orphans
