.PHONY: build up down logs

COMPOSE_CMD = docker-compose
COMPOSE_FILES = -f docker-compose.yml

build:
	$(COMPOSE_CMD) $(COMPOSE_FILES) build

up: build
	$(COMPOSE_CMD) $(COMPOSE_FILES) up

down:
	$(COMPOSE_CMD) $(COMPOSE_FILES) down

logs:
	$(COMPOSE_CMD) $(COMPOSE_FILES) logs -f
