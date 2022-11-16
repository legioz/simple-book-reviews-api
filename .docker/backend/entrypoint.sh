#!/bin/bash

cd /code/book_review/

printf "\n\n>>> Current dir"
pwd

ls -lh

printf "\n\n>>> Collect static files..."
python manage.py collectstatic --noinput

printf "\n\n>>> Apply database migrations..."
python manage.py migrate

printf "\n\n >>> Creating default superuser"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@admin.com', 'admin')" | python manage.py shell

printf "\n\n>>> Gunicorn Runserver..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload
