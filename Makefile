clean:
	rm -f db.sqlite3

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	gulp css
	python manage.py runserver

install:
	pip install -r requirements.txt
	npm install
	python manage.py syncdb

all: run