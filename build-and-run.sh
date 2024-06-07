#!/bin/bash

# Default project name
PROJECT_NAME=${1:-my_custom_app}

# Build the Docker image with the specified project name
docker build --build-arg PROJECT_NAME=${PROJECT_NAME} -t ${PROJECT_NAME} .

# Run the Docker container with the specified project name
docker run -it --rm -p 8000:8000 ${PROJECT_NAME}