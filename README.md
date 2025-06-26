# Go Quiz API

A quiz API built with Go for the **Mastering GitHub Copilot Agent Mode for Go Backend Developers** quest.

## 🚀 Getting Started

This repository is intentionally minimal - use GitHub Copilot Agent Mode to build the complete application!

### Quick Start

1. **Open in Codespace** or clone locally
2. **Open GitHub Copilot Chat** in VS Code
3. **Switch to Agent Mode** from the dropdown
4. **Start developing**:

   ```bash
   # The environment auto-starts with:
   # ✅ Go 1.21 development container
   # ✅ PostgreSQL database
   # ✅ Wilco agent for quest tracking
   # ✅ Hot reload with Air

   # Start coding with hot reload
   go-run
   ```

### Architecture

This starter uses a multi-container devcontainer setup:

- **Go Dev Container**: Official Go 1.21 image with full development tools
- **PostgreSQL**: Database service for your quiz API
- **Wilco Agent**: Quest tracking and guidance (sidecar container)

### Sample Application

The starter includes a minimal Go API:

- **GET /** - Simple "Hello" endpoint
- **Database connection** - Ready to connect to PostgreSQL
- **Hot reload** - Automatic restart on code changes

### Development Commands

Available aliases:

- `go-run` - Start with hot reload (Air)
- `go-build` - Build the application
- `go-test` - Run tests
- `go-mod` - Manage Go modules

**Ready to start?** Open Copilot Chat, enable Agent Mode, and begin building! 🚀

- **Wilco Agent**: Quest progress tracking

### Sample Application

The starter includes a minimal Go HTTP server:

- **GET /** - Simple welcome message
- **Database connection** - Ready to use with PostgreSQL

### Development Commands

Use these helpful aliases:

- `go-run` - Start with hot reload (Air)
- `go-build` - Build the application
- `go-test` - Run tests
- `go-mod` - Manage Go modules

### Database Connection

PostgreSQL is pre-configured and ready:

- Host: `postgres`
- Port: `5432`
- Database: `quiz_db`
- User: `quiz_user`
- Password: `quiz_password`

**Ready to start?** Open Copilot Chat, enable Agent Mode, and begin building! 🚀
