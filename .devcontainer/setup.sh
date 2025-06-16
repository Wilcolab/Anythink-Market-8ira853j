WILCO_ID="`cat .wilco`"
export ENGINE_EVENT_ENDPOINT="${ENGINE_BASE_URL}/users/${WILCO_ID}/event"

# Update engine that codespace started for user
curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" -H "Content-Type: application/json" --data-raw "{ \"event\": \"github_codespace_started\" }"

# Export welcome prompt in bash:
echo "printf \"\n\n☁️☁️☁️️ Develop in the Cloud ☁️☁️☁️\n\"" >> ~/.bashrc

nohup bash -c "cd /wilco-agent && node agent.js &" >> /tmp/agent.log 2>&1

# Install MongoDB - check if GPG key exists first
if [ ! -f "/usr/share/keyrings/mongodb-server-7.0.gpg" ]; then
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
    echo "MongoDB GPG key installed"
else
    echo "MongoDB GPG key already exists, skipping..."
fi

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Create the MongoDB data directory
sudo mkdir -p /data/db
sudo chown -R vscode:vscode /data/db

# Function to check if MongoDB is already running
is_mongodb_running() {
    mongosh --eval "db.runCommand({ ping: 1 })" >/dev/null 2>&1
    return $?
}

# Function to start MongoDB
start_mongodb() {
    # If MongoDB is already running, don't start it again
    if is_mongodb_running; then
        echo "MongoDB is already running"
        return 0
    fi

    # Clear the log file
    > /tmp/mongodb.log

    # Start MongoDB with proper options
    mongod --dbpath /data/db --fork --logpath /tmp/mongodb.log

    # Wait for MongoDB to start and be ready
    for i in {1..30}; do
        if is_mongodb_running; then
            echo "MongoDB started successfully"
            return 0
        fi
        sleep 1
    done

    echo "MongoDB failed to start within 30 seconds"
    return 1
}

# Start MongoDB
start_mongodb

# Print welcome message
echo "MongoDB development environment is ready! You can now use 'mongosh' to connect."