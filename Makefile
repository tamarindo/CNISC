clean:
	rm -f db.sqlite3

migrate:
	python manage.py makemigrations
	python manage.py makemigrations main
	python manage.py makemigrations messaging
	python manage.py makemigrations oauthSocial
	python manage.py makemigrations parceadores
	python manage.py makemigrations tags
	python manage.py makemigrations userManager
	python manage.py migrate

run:
	python manage.py runserver

install:
	pip install -r requirements.txt
	npm install
	python manage.py syncdb

all: run