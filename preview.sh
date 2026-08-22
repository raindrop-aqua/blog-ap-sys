#!/bin/sh
set -e

cd "$(dirname "$0")"

IMAGE_NAME="blog-preview"
CONTAINER_NAME="blog-preview"

container build -t "$IMAGE_NAME" .

container run --rm -p 4000:4000 \
  -v "$(pwd)":/srv/jekyll \
  --name "$CONTAINER_NAME" \
  "$IMAGE_NAME"
