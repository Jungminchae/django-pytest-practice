#!/bin/bash

./wait-for-it.sh db:5432 -- echo "Database is up!"

python src/manage.py makemigrations
python src/manage.py migrate

exec "$@"