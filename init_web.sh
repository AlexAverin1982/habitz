#!/bin/sh
echo 'making migrations....'
python manage.py makemigrations
echo 'migrating....'
python manage.py migrate