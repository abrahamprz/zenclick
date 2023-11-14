# Usage:
# make -f Makefile <command>

up:
	docker compose -f production.yml up -d

build:
	docker compose -f production.yml build

down:
	docker compose -f production.yml down

restart:
	docker compose -f production.yml down
	docker compose -f production.yml up -d

rebuild:
	docker compose -f production.yml down
	docker compose -f production.yml build
	docker compose -f production.yml up -d

shell:
    docker compose -f production.yml run --rm django /bin/sh

# Example: make run cmd=python manage.py migrate
run:
	docker compose -f production.yml run --rm $(shell echo $(cmd))

# Example: make manage cmd=migrate
manage:
	docker compose -f production.yml run --rm django python manage.py $(shell echo $(cmd))

migrations:
	docker compose -f production.yml run --rm django python manage.py makemigrations

migrate:
	docker compose -f production.yml run --rm django python manage.py migrate

createreport:
	docker compose -f production.yml run --rm django python manage.py createreport

collectstatic:
    docker compose -f production.yml run --rm django python manage.py collectstatic --no-input

# Local commands

up_local:
	docker compose -f local.yml up -d

build_local:
	docker compose -f local.yml build

down_local:
	docker compose -f local.yml down

restart_local:
	docker compose -f local.yml down
	docker compose -f local.yml up -d

rebuild_local:
	docker compose -f local.yml down
	docker compose -f local.yml build
	docker compose -f local.yml up -d

shell_local:
    docker compose -f local.yml run --rm django /bin/sh

# Example: make run_local cmd=python manage.py migrate
run_local:
	docker compose -f local.yml run --rm $(shell echo $(cmd))

# Example: make manage_local cmd=migrate
manage_local:
	docker compose -f local.yml run --rm django python manage.py $(shell echo $(cmd))

migrations_local:
	docker compose -f local.yml run --rm django python manage.py makemigrations

migrate_local:
	docker compose -f local.yml run --rm django python manage.py migrate

createreport_local:
	docker compose -f local.yml run --rm django python manage.py createreport

collectstatic_local:
    docker compose -f local.yml run --rm django python manage.py collectstatic --no-input
