clean:
	rm -f db.sqlite3

sync:
	pip install -r requirements.txt
	npm install
	python manage.py syncdb
	python manage.py migrate --noinput
	python manage.py migrate main --noinput

all: sync