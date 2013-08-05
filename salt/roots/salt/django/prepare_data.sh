#!/bin/bash

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
{{ venv.path }}/bin/python manage.py loaddata auth.json
{{ venv.path }}/bin/python manage.py manage_index create
{{ venv.path }}/bin/python manage.py import_services
{{ venv.path }}/bin/python manage.py import_bagni
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput
{{ venv.path }}/bin/python manage.py makemessages -a
{{ venv.path }}/bin/python manage.py compilemessages -a
