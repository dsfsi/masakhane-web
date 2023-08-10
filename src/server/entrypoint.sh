#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started 2"
fi

python manage.py create_db

echo "Loading some default models ..."
python manage.py add_language en-sw-JW300
python manage.py add_language en-af-JW300
python manage.py add_language en-luo-JW300

# wget http://localhost:5000/update

echo "Loading completed"

exec "$@"