#!/usr/bin/env bash

python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt
src/manage.py makemigrations
src/manage.py migrate

src/manage.py runserver