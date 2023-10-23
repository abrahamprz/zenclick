# Usage:
# make -f Makefile <command>

up:
	docker compose -f local.yml up

# Example: make run cmd=python manage.py migrate
run:
	docker compose -f local.yml run --rm $(shell echo $(cmd))

# Example: make manage cmd=migrate
manage:
	docker compose -f local.yml run --rm django python manage.py $(shell echo $(cmd))

migrations:
	docker compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm django python manage.py migrate

build:
	docker compose -f local.yml up --build