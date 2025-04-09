# Drivenets Router Management Application

This project consists of a React frontend application and a mock backend server using json-server for the Drivenets Router Management interview application.

## Description

The Drivenets Router Management Backend is a simple REST API server that simulates a backend for router management operations. It uses json-server to provide a fully functioning REST API based on a JSON file that serves as the database.

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Installation & Setup

1. Install backend dependencies:

```bash
cd backend
npm install
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:

```bash
cd backend
npm start
```

The API will be available at port 3001

2. In a new terminal, start the frontend application:

```bash
cd frontend
npm start
```

The frontend will be available at port 3000

### API Endpoints

RESTful routes for the routers are available at `/routers`.

for example:

```json
[
  {
    "id": "r-000001",
    "name": "Regional Gateway",
    "type": "enterprise",
    "createdAt": "2022-10-15T09:34:33.000Z",
    "updatedAt": "2023-06-01T07:55:51.774Z",
    "coordinates": {
      "latitude": 80.9654,
      "longitude": -13.3508
    },
    "portCount": 127,
    "supportedProtocols": ["RIP", "BGP", "HSRP", "LISP", "OSPF", "PIM"],
    "throughputGbps": 40
  },
  {
    "id": "r-000003",
    "name": "Personal WiFi",
    "type": "home",
    "createdAt": "2022-10-08T23:48:06.000Z",
    "updatedAt": "2024-12-12T17:39:43.240Z",
    "coordinates": {
      "latitude": -25.842,
      "longitude": 54.3554
    },
    "connectedDevices": 25,
    "parentalControlsEnabled": false,
    "maxBandwidthMbps": 1000
  },
  {
    "id": "r-000006",
    "name": "High-Speed Access Point",
    "type": "wifi",
    "createdAt": "2022-01-08T07:06:11.000Z",
    "updatedAt": "2024-04-28T21:52:28.723Z",
    "coordinates": {
      "latitude": -38.3813,
      "longitude": 156.3821
    },
    "wifiChannels": [4, 20, 33, 16],
    "supportsDualBand": true
  }
]
```

You would have the following endpoints:

- `GET /routers` - Get all routers
- `GET /routers/1` - Get router with id 1
- `POST /routers` - Create a new router
- `PUT /routers/1` - Update router with id 1
- `PATCH /routers/1` - Partially update router with id 1
- `DELETE /routers/1` - Delete router with id 1

Similar endpoints would be available for interfaces.
