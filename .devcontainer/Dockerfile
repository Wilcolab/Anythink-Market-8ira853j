FROM mcr.microsoft.com/devcontainers/go:1-1.24-bookworm

# Pre-install Air for hot reloading to avoid doing it every startup
RUN go install github.com/air-verse/air@latest

# Create workspace directory
RUN mkdir -p /workspaces

# Set working directory
WORKDIR /workspaces

# Copy go.mod and go.sum first for better layer caching
COPY go.mod go.sum ./

# Download dependencies (this will be cached if go.mod/go.sum don't change)
RUN go mod download

# Copy the rest of the application
COPY . .

# Run go mod tidy to ensure everything is clean
RUN go mod tidy
