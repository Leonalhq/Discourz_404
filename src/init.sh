#! /bin/bash

# A script that automates the reconstruction of the entire database.
pip install channels
pip install service_identity
rm -f db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < init.py
