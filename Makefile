## ------------ SCRIPTS ------------
script:
	scripts/index.sh

## ------------- LOCAL -------------
up:
	docker-compose -p backend -f local.yml up -d
build:
	docker-compose -p backend -f local.yml up -d --build
down:
	docker-compose -p backend -f local.yml down -v
start:
	docker-compose -p backend -f local.yml start
stop:
	docker-compose -p backend -f local.yml stop
restart:
	docker-compose -p backend -f local.yml restart $(service)
recreate:
	docker-compose -p backend -f local.yml up -d --force-recreate django
rebuild:
	docker-compose -p backend -f local.yml down -v && docker-compose -p backend -f local.yml up -d --build
test:
	docker-compose -p backend -f local.yml exec django pytest -v $(target)
migrate:
	docker-compose -p backend -f local.yml exec django python manage.py migrate
makemigrations:
	docker-compose -p backend -f local.yml exec django python manage.py makemigrations
createsuperuser:
	docker-compose -p backend -f local.yml exec django python manage.py createsuperuser
pre-commit:
	docker-compose -p backend -f local.yml exec django pre-commit run -a
