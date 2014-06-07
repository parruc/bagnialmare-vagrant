{% set venv = pillar.venv.venvs[django_name] %}
{% set django = pillar.django.djangos[django_name] %}
{% set user = pillar.users[django_name] %}

cd {{ django.path }}
sudo -u {{ user.name }} {{ venv.path }}/bin/python manage.py dumpdata --indent=2 --natural --exclude sessions --exclude admin --exclude contenttypes --exclude auth.Permission > ombrelloni/fixtures/dump.json
git commit ombrelloni/fixtures/* -m "data json dump"
git push
