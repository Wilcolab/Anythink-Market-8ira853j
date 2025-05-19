#!/bin/bash

WILCO_ID="`cat .wilco`"
CODESPACE_BACKEND_HOST=$(curl -s "${ENGINE_BASE_URL}/api/v1/codespace/backendHost?codespaceName=${CODESPACE_NAME}&portForwarding=${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}" | jq -r '.codespaceBackendHost')
CODESPACE_BACKEND_URL="https://${CODESPACE_BACKEND_HOST}"
export ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"

# Install Amazon Q CLI
echo "Installing Amazon Q CLI..."
export AMAZON_Q_VERSION=latest && \
    curl --proto '=https' --tlsv1.2 -sSf "https://desktop-release.q.us-east-1.amazonaws.com/${AMAZON_Q_VERSION}/amazon-q.deb" -o amazon-q.deb && \
    sudo apt-get update && \
    sudo apt-get install -y ./amazon-q.deb && \
    rm ./amazon-q.deb && \
    sudo rm -rf /var/lib/apt/lists/*

# Update engine that codespace started for user
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" -H "Content-Type: application/json" --data-raw "{ \"event\": \"github_codespace_started\" }"