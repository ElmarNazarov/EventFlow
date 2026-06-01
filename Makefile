.PHONY: up down build logs api-shell frontend-shell migrate makemigration seed test lint format

COMPOSE = docker compose

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

api-shell:
	$(COMPOSE) exec api bash

frontend-shell:
	$(COMPOSE) exec frontend sh

migrate:
	$(COMPOSE) exec api alembic upgrade head

makemigration:
	$(COMPOSE) exec api alembic revision --autogenerate -m "$(msg)"

seed:
	@echo "Seed data will be available in Milestone 9"

test:
	$(COMPOSE) exec api pytest -v

lint:
	$(COMPOSE) exec api ruff check app

format:
	$(COMPOSE) exec api ruff format app
