#!/bin/bash

# Try to verify Q installation and configuration
Q_STATUS=$(q doctor 2>&1)
if echo "$Q_STATUS" | grep -q "Doctor found errors"; then
    echo "Q is not properly configured: $Q_STATUS"
    exit 1
fi


: ${ENGINE_BASE_URL:="https://engine.wilco.gg"}
WILCO_ID="`cat .wilco`"
export ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"

# Send verification event to server
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" \
    -H "Content-Type: application/json" \
    --data-raw "{ \"event\": \"amazon_q_configuration_verified\", \"metadata\": {\"status\": \"success\" }}"

echo "Q configuration verified successfully, you can now go back to chat."
