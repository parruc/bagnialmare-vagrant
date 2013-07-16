#!/bin/bash

{{ venv.path }}/bin/python manage.py syncdb --noinput --migrate
{{ venv.path }}/bin/python manage.py loaddata auth.json
{{ venv.path }}/bin/python manage.py loaddata bagni.json
{{ venv.path }}/bin/python manage.py rebuild_index --noinput
{{ venv.path }}/bin/python manage.py collectstatic -l --noinput