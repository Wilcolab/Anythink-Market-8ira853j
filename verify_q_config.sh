#!/bin/bash

# Try to get Q configuration status
Q_STATUS=$(aws q get-configuration 2>&1)
if [ $? -ne 0 ]; then
    echo "Q is not properly configured: $Q_STATUS"
    exit 1
fi


WILCO_ID="`cat .wilco`"
export ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"

# Send verification event to server
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" \
    -H "Content-Type: application/json" \
    --data-raw "{ \"event\": \"q_configuration_verified\", \"metadata\": {\"status\": \"success\", \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\" }}"

echo "Q configuration verified successfully, you can now go back to chat."
