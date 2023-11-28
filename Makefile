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
test:
	docker-compose -f local.yml run --rm django python manage.py test
createsuperuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser
loaddata:
	docker-compose -f local.yml run --rm django python manage.py loaddata omnihr_assignment/employee/fixtures/initial_data.json && docker-compose -f local.yml run --rm django python manage.py loaddata omnihr_assignment/users/fixtures/company.json
