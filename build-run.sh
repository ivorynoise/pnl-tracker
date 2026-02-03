#!/bin/bash
set -e

# REGISTRY=""
IMAGE_NAME="ivorynoise/pnl-tracker"

echo "Building Docker image..."
docker build --platform=linux/amd64 -t "$IMAGE_NAME:latest" .

# I used to push it to dockerhub
echo "Pushing Docker image to registry..."
read -p "Enter tag to push (e.g., 1.0.0-dev, or 'skip' to skip pushing): " TAG
docker tag "$IMAGE_NAME:latest" "$IMAGE_NAME:$TAG"
docker push "$IMAGE_NAME:$TAG"
docker push "$IMAGE_NAME:latest"


echo "Done! Image pushed: $IMAGE_NAME:$TAG"