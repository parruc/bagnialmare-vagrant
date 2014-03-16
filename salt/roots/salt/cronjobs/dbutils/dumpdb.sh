{% set db = pillar.pg.dbs[django_name] %}
{% set user = pillar.users[django_name] %}
{% set db_user = pillar.users['postgres'] %}

sudo -u {{ db_user.name }} pg_dump {{ db.name }} > ombrelloni/fixtures/dump.sql
chown {{ user.name }}:{{ user.group }} ombrelloni/fixtures/dump.sql
git commit ombrelloni/fixtures/* -m "db dump"
