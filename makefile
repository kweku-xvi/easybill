rs:
	@python manage.py runserver

mm:
	@python manage.py makemigrations

m:
	@python manage.py migrate

su:
	@python manage.py createsuperuser