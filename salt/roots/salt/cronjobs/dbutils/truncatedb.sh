{% set venv = pillar.venv.venvs[django_name] %}

{{ venv.path }}/bin/python manage.py sqlflush | sed 's/TRUNCATE \(.*\);/TRUNCATE \1 CASCADE;/g' | {{ venv.path }}/bin/python manage.py dbshell
