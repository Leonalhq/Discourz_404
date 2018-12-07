#! /bin/bash

# A script that automates the reconstruction of the entire database.
rm -f db.sqlite3
py manage.py makemigrations
py manage.py migrate
py manage.py shell < init.py
