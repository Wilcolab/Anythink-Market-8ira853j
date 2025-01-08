# RiskiStore

A modern e-commerce web application built with a robust tech stack. The frontend is developed using React with TypeScript for type safety and better developer experience, powered by Vite for lightning-fast builds. The backend is built with NestJS, a progressive Node.js framework, with PostgreSQL as the database and Apache Kafka for event streaming. The entire application is containerized using Docker for consistent development and deployment environments.

## Project Structure

```
riskistore/
├── frontend/         # React + TypeScript frontend application (Vite)
├── backend/         # NestJS backend service
└── docker-compose.yml
```

## Prerequisites

- GitHub Codespaces
- Docker and Docker Compose (pre-installed in Codespace)

## Getting Started

The application is configured to run in GitHub Codespaces environment. Once your Codespace is ready:

1. Start the application using Docker Compose:
```bash
docker-compose up
```

This will start:
- Frontend development server with hot-reload
- Backend API service
- PostgreSQL database
- Kafka and Zookeeper services

The frontend will be available at the automatically forwarded port, typically `3000`.
The backend API will be accessible at `3001`.

## Development

### Frontend
The frontend application is located in the `frontend/` directory. It's built with:
- React
- TypeScript
- Vite for fast development and optimized builds
- Hot-reload enabled for quick development iterations

### Backend
The backend application is located in the `backend/` directory. It features:
- NestJS framework
- TypeScript
- PostgreSQL database
- Kafka integration for event streaming
- RESTful API endpoints with built-in OpenAPI (Swagger) documentation

## Docker Configuration

The project includes:
- `docker-compose.yml` - Main Docker Compose configuration
- `frontend/Dockerfile.dev` - Frontend development container configuration
- `backend/Dockerfile.dev` - Backend development container configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
