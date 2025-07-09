#!/bin/bash
set -e

if [ -z "$DOCKER_PASSWORD" ]; then
  echo "Error: DOCKER_PASSWORD is not set."
  exit 1
fi

echo "$DOCKER_PASSWORD" | docker login --username secdevias --password-stdin

imgName="hikari-ctfd"
imgVersion="0.0.2"
docker build --label "$imgName" --tag "$imgName:$imgVersion" .

docker tag "$imgName:$imgVersion" secdevias/"$imgName:$imgVersion"
docker push secdevias/"$imgName:$imgVersion"

echo "Generating SecDevias-Torii Image....[Done]"
echo "---------------------------------------------------"
echo "| IMAGE secdevias/${imgName}:${imgVersion} - DONE"
echo "---------------------------------------------------"
docker logout


