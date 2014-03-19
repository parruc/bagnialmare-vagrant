#!/bin/bash

{% set db = pillar.pg.dbs[django_name] %}
{% set venv = pillar.venv.venvs[django_name] %}
{% set db_user = pillar.users['postgres'] %}
{% set user = pillar.users[django_name] %}

sudo -u {{ db_user.name }} dropdb {{ db.name }}
cat ombrelloni/fixtures/dump.sql | sudo -u {{ db_user.name }} psql
sudo -u {{ user.name }} {{ venv.path }}/bin/python manage.py migrate
sudo -u {{ user.name }} {{ venv.path }}/bin/python manage.py manage_index -o rebuild
