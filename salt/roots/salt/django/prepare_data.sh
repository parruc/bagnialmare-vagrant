#!/bin/bash

{% set venv = pillar.venv.venvs[django_name] %}
{% set loc = grains['configuration'] in ['local'] %}

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
{{ venv.path }}/bin/python manage.py manage_index -o create
{{ venv.path }}/bin/python manage.py collectstatic --noinput
{{ venv.path }}/bin/python manage.py compilemessages
{{ venv.path }}/bin/python manage.py manage_index -o rebuild

# Opbeat release notification
curl https://opbeat.com/api/v1/organizations/7eecea6e5ebd44a5843b5722fa313184/apps/fac46f5ccf/releases/ \
    -H "Authorization: Bearer 58e1cadb5eb47e2e36282fb8d6d0951407924fdc" \
    -d rev=`git log -n 1 --pretty=format:%H` \
    -d branch=`git rev-parse --abbrev-ref HEAD` \
    -d status=completed
