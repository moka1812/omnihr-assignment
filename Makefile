dev:
	docker-compose -f local.yml up
migrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations
migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate
shell:
	docker-compose -f local.yml run --rm django python manage.py shell
dev.build:
	docker-compose -f local.yml up --build	
