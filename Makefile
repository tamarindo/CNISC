clean:
	rm -f db.sqlite3

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	gulp css
	python manage.py runserver 0.0.0.0:8000

install:
	pip install -r requirements.txt
	sudo npm -g gulp
	sudo npm -g bower
	npm install
	bower install
	python manage.py syncdb
	python manage.py loaddata ./fixtures/perfiles.json
	python manage.py loaddata ./fixtures/oauthSOcial.json
	python manage.py loaddata ./fixtures/user.json
	
all: run
