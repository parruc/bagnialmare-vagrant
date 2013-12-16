#!/bin/bash

{% set venv = pillar.venv.venvs[django_name] %}

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
{{ venv.path }}/bin/python manage.py manage_index -o create
{{ venv.path }}/bin/python manage.py loaddata dump.json
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput
{{ venv.path }}/bin/python manage.py compilemessages
{{ venv.path }}/bin/python manage.py manage_index -o rebuild
