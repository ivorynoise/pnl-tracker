#!/bin/bash
set -e

IMAGE_NAME="ivorynoise/pnl-tracker:latest"

echo "Building Docker image..."
docker build --platform=linux/amd64 -t "$IMAGE_NAME" .

echo "Pushing Docker image to registry..."
docker push "$IMAGE_NAME"

echo "Done! Image pushed: $IMAGE_NAME"
