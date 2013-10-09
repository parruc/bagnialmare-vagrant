#!/bin/bash

{{ venv.path }}/bin/python manage.py syncdb --noinput
{{ venv.path }}/bin/python manage.py migrate
{{ venv.path }}/bin/python manage.py loaddata auth.json
{{ venv.path }}/bin/python manage.py manage_index -o create
{{ venv.path }}/bin/python manage.py import_services
{{ venv.path }}/bin/python manage.py import_bagni
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput
{{ venv.path }}/bin/python manage.py compilemessages
{{ venv.path }}/bin/python manage.py sync_translation_fields --noinput
{{ venv.path }}/bin/python manage.py update_translation_fields