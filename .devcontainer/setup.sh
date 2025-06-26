#!/bin/bash

echo "🚀 Setting up Go development environment..."

# Wilco-specific setup (runs in wilco-agent container)
WILCO_ID="`cat .wilco 2>/dev/null || echo 'unknown'`"

# Update engine that codespace started for user (if in Codespaces)
if [ "$CODESPACE_NAME" ]; then
    curl -L -X POST "${ENGINE_EVENT_ENDPOINT}" -H "Content-Type: application/json" --data-raw "{ \"event\": \"github_codespace_started\" }" 2>/dev/null || true
fi

# Initialize Go module if it doesn't exist
if [ ! -f "go.mod" ]; then
    echo "📦 Initializing Go module..."
    go mod init go-quiz-api
fi

# Install Air for hot reloading
echo "🔄 Installing Air for hot reloading..."
go install github.com/cosmtrek/air@latest

# Configure Codespace ports (if in Codespaces)
if [ "$CODESPACE_NAME" ]; then
    gh codespace ports visibility 8080:public --codespace $CODESPACE_NAME 2>/dev/null || true
    gh codespace ports visibility 3009:public --codespace $CODESPACE_NAME 2>/dev/null || true
fi

# Add helpful aliases for Go development
echo "alias go-run='air'" >> ~/.bashrc
echo "alias go-build='go build .'" >> ~/.bashrc
echo "alias go-test='go test ./...'" >> ~/.bashrc
echo "alias go-mod='go mod'" >> ~/.bashrc

# Welcome message
echo "printf \"\n🐹 Go Development Ready! Database running. Use GitHub Copilot Agent Mode!\n\"" >> ~/.bashrc
echo "printf \"💡 Use 'go-run' to start with hot reload\n\"" >> ~/.bashrc

echo "✅ Setup complete!"