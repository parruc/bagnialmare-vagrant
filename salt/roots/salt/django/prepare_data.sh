#!/bin/bash

{% set venv = pillar.venv.venvs[django_name] %}
{% set loc = grains['configuration'] in ['local'] %}

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
{{ venv.path }}/bin/python manage.py manage_index -o create
{% if loc %}
{{ venv.path }}/bin/python manage.py loaddata dump.json
{% else %}
echo "NOT IMPORTING DATA OUTSIDE LOCAL BOX TO AVOID OVERRIDE"
{% endif %}
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput
{{ venv.path }}/bin/python manage.py compilemessages
{{ venv.path }}/bin/python manage.py manage_index -o rebuild
