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
**Command Submission & Persistence:**
The client sends a command (a sequence of actions). The application stores it in the database and returns a unique command ID. The command is queued for later processing — avoiding long-lived HTTP connections and improving fault tolerance.

**Command Parsing:**
A dedicated worker retrieves queued commands, splits them into individual actions, and saves these in the database. This is done within a single transaction, ensuring either all actions are stored or none at all (atomicity).

**Action Execution:**
Another worker processes the actions in order and sends them to the robot.
If an obstacle is encountered, remaining actions in the command are marked WITHDRAWN to prevent the robot from getting stuck and to allow for re-planning.


## Implementation Logic and Design Rationale
This system’s architecture is driven by two critical factors:

- **We cannot keep HTTP connections open for a long time.**

   Executing commands synchronously during an HTTP request is not feasible due to possible timeouts and connection interruptions.

- **The system must maintain up-to-date robot position data across restarts.**

   Whether during planned restarts or unexpected shutdowns (e.g., power loss), the robot’s state must be preserved to avoid data loss and ensure smooth continuation.

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