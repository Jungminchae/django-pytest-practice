#!/bin/bash

./wait-for-it.sh db:5432 -- echo "Database is up!"

python app/src/manage.py makemigrations
python app/src/manage.py migrate

exec "$@"