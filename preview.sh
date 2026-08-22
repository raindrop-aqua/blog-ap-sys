#!/bin/sh
set -e

cd "$(dirname "$0")"

IMAGE_NAME="blog-preview"
CONTAINER_NAME="blog-preview"

container build -t "$IMAGE_NAME" .

# 既に同名のコンテナが起動/存在している場合は先に削除する
container delete -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

container run --rm -p 4000:4000 \
  -v "$(pwd)":/srv/jekyll \
  --name "$CONTAINER_NAME" \
  "$IMAGE_NAME"
