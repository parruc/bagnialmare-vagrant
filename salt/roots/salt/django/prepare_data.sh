#!/bin/bash

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
#TODO: CLEAR DEI DATI SOLO SE IN PRODUZIONE?
{{ venv.path }}/bin/python manage.py loaddata auth.json
{{ venv.path }}/bin/python manage.py import_services
{{ venv.path }}/bin/python manage.py import_bagni
{{ venv.path }}/bin/python manage.py rebuild_index --noinput
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput
