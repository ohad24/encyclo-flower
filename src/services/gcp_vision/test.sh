#!/bin/bash

set -e

b64_image=$(base64 ../../../tests/assets/images/58NY77V207Q7H06.jpg)

echo '{"encoded_image": "'"$b64_image"'"}' | \
  curl -s -X 'POST' 'http://localhost:5001/detect/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @- | jq
