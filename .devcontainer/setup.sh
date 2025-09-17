WILCO_ID="`cat .wilco`"

export ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"

# Update engine that codespace started for user
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" -H "Content-Type: application/json" --data-raw "{ \"event\": \"github_codespace_started\" }"

gh codespace ports visibility 3000:public --codespace $CODESPACE_NAME
gh codespace ports visibility 3001:public --codespace $CODESPACE_NAME

CODESPACE_BACKEND_URL="https://${CODESPACE_NAME}-3001.app.github.dev"
echo "export CODESPACE_BACKEND_URL=\"${CODESPACE_BACKEND_URL}\"" >> ~/.bashrc
echo "export REACT_APP_CODESPACE_BACKEND_URL=\"${CODESPACE_BACKEND_URL}\"" >> ~/.bashrc

# Export welcome prompt in bash:
echo "printf \"\n\n☁️☁️☁️️ Wilco: Develop in the Cloud ☁️☁️☁️\n\"" >> ~/.bashrc

nohup bash -c "cd /wilco-agent && node agent.js &" >> /tmp/agent.log 2>&1