#!/usr/bin/env bash
set -e

IMAGE_NAME="fc26-chatbot"

# Build the image
docker build -t $IMAGE_NAME .

# Run the container
docker run --rm -p 5001:5001 $IMAGE_NAME
