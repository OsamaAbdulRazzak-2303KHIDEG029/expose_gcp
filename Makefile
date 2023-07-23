# Docker Compose command
DOCKER_COMPOSE = docker-compose

# Targets

.PHONY: build
build:
	$(DOCKER_COMPOSE) build

.PHONY: up
up:
	$(DOCKER_COMPOSE) up

.PHONY: down
down:
	$(DOCKER_COMPOSE) down

.PHONY: start
start:
	$(DOCKER_COMPOSE) start

.PHONY: stop
stop:
	$(DOCKER_COMPOSE) stop

.PHONY: restart
restart:
	$(DOCKER_COMPOSE) restart

.PHONY: etl
etl:
	$(DOCKER_COMPOSE) run etl_service python etl_script.py

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

.PHONY: shell
shell:
	$(DOCKER_COMPOSE) run etl_service bash

.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans
