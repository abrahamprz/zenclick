CURRENT_DIRECTORY := $(shell pwd)

TESTSCOPE = .
TESTFLAGS =

help:
		@echo "Docker Compose Help"
		@echo "-----------------------"
		@echo ""
		@echo "Run tests to ensure current state is good:"
		@echo "    make test"
		@echo ""
		@echo "If tests pass, add fixture data and start up the django:"
		@echo "    make begin"
		@echo ""
		@echo "Really, really start over:"
		@echo "    make clean"
		@echo ""
		@echo "See contents of Makefile for more targets."

begin: migrate fixtures start

dev:
		@docker compose run --rm --service-ports django python manage.py runserver_plus 0.0.0.0:8000


start:
		@docker compose up -d

stop:
		@docker compose stop

status:
		@docker compose ps

restart: stop start

clean: stop
		@docker compose rm --force
		@find . -name \*.pyc -delete

build:
		@docker compose down
		@git pull
		@docker compose build

build_no_pull:
		@docker compose down
		@docker compose build

rebuild: build start

test:
		@docker compose run --rm django pytest ${TESTSCOPE} ${TESTFLAGS}

cov:
		@docker compose run --rm django coverage run -m pytest

report:
		@docker compose run --rm django coverage report

migrate:
		@docker compose run --rm django python ./manage.py migrate

makemigrations:
		@docker compose run --rm django python ./manage.py makemigrations

cli:
		@docker compose run --rm django /bin/sh

tail:
		@docker compose logs -f

token:
		@docker compose run --rm django python refresh_service_token.py

pycharm:
		@docker ps -a | grep -i pycharm | awk '{print $1}' | xargs docker rm

get_celery_tasks:
		@docker compose run --rm django celery inspect registered

backup:
		@docker compose run --rm postgres backup

upload:
		@docker compose run --rm awscli upload

list_backups:
		@docker compose run --rm postgres backups

run:
		@docker compose run --rm django python manage.py $(cmd)

lint:
		docker compose run --rm django python -m ruff check --fix

format:
		docker compose run --rm django python -m ruff format

.PHONY: start stop status restart clean build rebuild test cov report migrate makemigrations
.PHONY: cli tail token sync set_homes update_counts sync_all initial_permissions pycharm update_carts
.PHONY: sync_full build_no_pull import_employees update_employees_task update_students_task synchronize_with_ad_task
.PHONY: backup list_backups run
