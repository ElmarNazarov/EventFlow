# EventFlow

Event-driven order and workflow processing platform — a senior-level full-stack portfolio project demonstrating production-style architecture with FastAPI, Next.js, PostgreSQL, Redis, RabbitMQ, and Kafka.

## Overview

EventFlow is an internal operations platform for managing customer orders, inventory reservations, payment processing, shipping workflows, event history, and background job orchestration. It is **not** an ecommerce storefront; it models the backend systems behind order fulfillment.

This repository is built incrementally across milestones.

- **Milestone 1** — Docker infrastructure, health checks, minimal frontend
- **Milestone 2** — JWT auth, roles, login, app shell
- **Milestone 3** — Orders and inventory CRUD with paginated APIs and dashboard UI
- **Milestone 4** — RabbitMQ command pipeline (inventory → payment → shipping workers)

## Features (planned across milestones)

- JWT authentication with role-based access control
- Order lifecycle management with event-driven workflows
- RabbitMQ command processing (inventory, payment, shipping)
- Kafka event streaming and event log
- Workflow state tracking with retry support
- Operations dashboard with analytics
- Background workers and event consumers

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | FastAPI, Python 3.12+, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Frontend | Next.js, TypeScript, Tailwind CSS, TanStack Query |
| Data | PostgreSQL 16, Redis 7 |
| Messaging | RabbitMQ, Apache Kafka |
| Infrastructure | Docker, Docker Compose |

## Local Development

1. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

2. Start all services:

   ```bash
   make build
   make up
   ```

3. Run database migrations and seed demo users:

   ```bash
   make migrate
   make seed
   ```

4. Open the applications:

   - API docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/v1/health
   - Frontend: http://localhost:3000 (or your `FRONTEND_HOST_PORT`)
   - Login: http://localhost:3000/login
   - RabbitMQ Management: http://localhost:15672 (guest / guest)
   - Kafka UI: http://localhost:8080

   If default host ports are already in use, set overrides in `.env` (see `.env.example`):
   `API_HOST_PORT`, `FRONTEND_HOST_PORT`, `POSTGRES_HOST_PORT`, `REDIS_HOST_PORT`.

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| api | 8000 | FastAPI application |
| frontend | 3000 | Next.js application |
| db | 5432 | PostgreSQL 16 |
| redis | 6379 (host default; use `REDIS_HOST_PORT` if busy) | Redis 7 |
| rabbitmq | 5672 | AMQP broker |
| rabbitmq (mgmt) | 15672 | Management UI |
| kafka | 9092 | Kafka broker |
| kafka-ui | 8080 | Kafka UI |
| worker | — | RabbitMQ command worker |
| event_consumer | — | Kafka event consumer |

## Environment Variables

See [`.env.example`](.env.example) for all configuration options. Key variables:

- `DATABASE_URL` — async PostgreSQL connection for the API
- `SYNC_DATABASE_URL` — sync connection for Alembic migrations
- `REDIS_URL`, `RABBITMQ_URL`, `KAFKA_BOOTSTRAP_SERVERS` — infrastructure endpoints
- `NEXT_PUBLIC_API_BASE_URL` — frontend API base URL

## Demo Users

After `make migrate` and `make seed`, use these accounts:

| Email | Password | Role |
|-------|----------|------|
| admin@eventflow.local | password123 | ADMIN |
| ops@eventflow.local | password123 | OPS_MANAGER |
| support@eventflow.local | password123 | SUPPORT |
| viewer@eventflow.local | password123 | VIEWER |

## Running Tests

Backend tests will be added in **Milestone 9**. For now:

```bash
make test
```

## Background Workers

- **worker** — consumes RabbitMQ commands (inventory, payment, shipping) — logic added in Milestone 4
- **event_consumer** — consumes Kafka events for event log projection — logic added in Milestone 5

## Project Structure

```text
EventFlow/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── docker/           # Docker-related configs
├── docker-compose.yml
├── Makefile
└── README.md
```

## Design Decisions

Design decisions documentation will expand as milestones are completed. See the full project specification for planned rationale (RabbitMQ for commands, Kafka for events, workflow tracking, etc.).

## Future Improvements

- Real payment and shipping provider integrations
- Dead-letter queues and advanced retry policies
- Distributed tracing (OpenTelemetry)
- Prometheus / Grafana monitoring
- Event replay and CQRS read models
- Multi-tenant workspace support
