# Moon Mission

Asynchronous command processing system to control a robot by executing sequences of actions step-by-step.

---

## Table of Contents

* [Overview](#overview)
* [System Architecture](#system-architecture)
* [Technology Stack](#technology-stack)
* [Workflow](#workflow)
* [API Endpoints](#api-endpoints)
* [Authentication](#authentication)
* [Getting Started](#getting-started)

---

## Overview

This project provides an API and worker system to receive, parse, and execute robot commands asynchronously. 
Commands are broken down into individual actions and processed stepwise by dedicated workers.

---

## System Architecture

* **API Server**: Receives command requests and returns command IDs.
* **Database**: Stores commands and their parsed actions.
* **Parsing Worker**: Parses commands into individual actions and saves them.
* **Execution Worker**: Sends parsed actions to the robot hardware for execution.

---

## Technology Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **Workers:** APScheduler
* **Migrations:** Alembic
* **Containerization:** Docker & Docker Compose

---

## Workflow

1. **Command Submission:**
   Client sends a command (sequence of actions) via API.

2. **Persistence:**
   API stores the command in the database and returns a unique command ID.

3. **Parsing:**
   Parsing worker retrieves the command, splits it into individual actions, and saves them.

4. **Execution:**
   Execution worker fetches actions and sends them to the robot hardware.

---

## Authentication

All API requests **must** include a valid Bearer token in the `Authorization` header.
Requests without a valid token will receive a `401 Unauthorized` response.

Example header:

```http
Authorization: Bearer <your_token_here>
```

---

## API Endpoints

### `GET /status`

Retrieve the current status of the robot.

* **Authentication:** Required (Bearer token)
* **Request example:**

  ```http
  GET /status HTTP/1.1
  Host: api.robot.com
  Authorization: Bearer <your_token_here>
  ```
* **Response:** Robot status details (position, direction, state, etc.)

---

### `POST /command`

Register a new command (set of actions) for the robot.

* **Authentication:** Required (Bearer token)
* **Request example:**

  ```http
  POST /command HTTP/1.1
  Host: api.robot.com
  Authorization: Bearer <your_token_here>
  Content-Type: application/json

  {
    "command": "FBFLFFRFF"
  }
  ```
* **Response:**

  ```json
  {
    "id": "<unique_command_id>"
  }
  ```

---

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Set environment variables:**

   ```
   POSTGRES_DSN=<your_postgres_dsn>
   START_POSITION=<start_x,start_y>
   START_DIRECTION=<start_direction>
   API_TOKEN=<your_api_token>
   ```

3. **Build and run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

4. **Access API documentation:**

   Once the application is running, open your browser at:
   ```bash
   http://localhost:8000/docs
   ```
   to explore the interactive Swagger UI.


## Run Unit Tests

You can run all unit tests using Python’s built-in `unittest` framework:

```
python -m unittest discover -s tests/unit_tests -v
```