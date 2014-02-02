{% set venv = pillar.venv.venvs[django_name] %}
{% set django = pillar.django.djangos[django_name] %}

cd {{ django.path }}
{{ venv.path }}/bin/python manage.py dumpdata --indent=2 > ombrelloni/fixtures/dump.json
{% for app in django.installed_apps %}
{{ venv.path }}/bin/python manage.py dumpdata {{app}} --natural --indent=2 > ombrelloni/fixtures/{{ app }}.json
{% endfor %}
git commit ombrelloni/fixtures/* -m "db dump"
git push
