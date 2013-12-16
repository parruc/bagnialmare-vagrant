{% set venv = pillar.venv.venvs[django_name] %}
{% set django = pillar.django.djangos[django_name] %}

cd {{ django.path }}
{{ venv.path }}/bin/python manage.py dumpdata --indent=2 > ombrelloni/fixtures/dump.json
git commit ombrelloni/fixtures/dump.json -m "db dump"
git push
