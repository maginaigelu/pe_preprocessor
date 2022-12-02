SHELL := /bin/bash

export COMPOSE_FILE=./ci/compose/docker-compose.yml


.PHONY: build up stop down ps bash _up_db list

build:
	@docker-compose build app

_up_db:
	@docker-compose up -d postgres
	@sleep 3

up: _up_db migrate
	@docker-compose up -d postgres pyspark rabbitmq app dramatiq

ps:
	@docker-compose ps

stop:
	@docker-compose stop

down:
	@docker-compose down

bash:
	@docker-compose run --rm app bash

makemigrations:
	@docker-compose run --rm app bash -c 'alembic revision --autogenerate -m "$(message)"'

migrate:
	@docker-compose run --rm app bash -c 'alembic upgrade head'

list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'