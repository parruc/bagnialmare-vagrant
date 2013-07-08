{% set user = pillar['users'].postgres %}

postgres_reqs:
    pkg:
        - installed
        - names:
            - postgresql-9.1
            - postgresql-server-dev-9.1
            - postgresql-contrib-9.1
            - postgresql-9.1-postgis

postgres_service:
    service.running:
        - name: postgresql
        - enable: True
        - sig: postgresql
        - require:
            - user: user_postgres
            - pkg: postgres_reqs
        - watch:
            - file: postgresql_conf
            - file: pg_hba_conf

postgresql_conf:
    file.managed:
        - source: salt://postgres/postgresql.conf
        - name: /etc/postgresql/9.1/main/postgresql.conf
        - template: jinja
        - context:
            pg: {{ pillar['pg'] }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 644
        - makedirs: True
        - replace: True
        - require:
            - user: user_postgres
            - pkg: postgres_reqs

pg_hba_conf:
    file.managed:
        - source: salt://postgres/pg_hba.conf
        - name: /etc/postgresql/9.1/main/pg_hba.conf
        - template: jinja
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 644
        - makedirs: True
        - replace: True
        - require:
            - user: user_postgres
            - pkg: postgres_reqs

{% for db_name, db in pillar['pg'].dbs.iteritems() %}
postgres_user_{{ db.owner }}:
    postgres_user.present:
        - name: {{ db.owner }}
        - password: {{ db.pass }}
        - runas: {{ user.name }}
        - require:
            - user: user_postgres
            - service: postgres_service

postgresql_database_{{ db_name }}:
    postgres_database.present:
        - name: {{ db.name }}
        - owner: {{ db.owner }}
        - template: template0
        - runas: {{ user.name }}
        - require:
            - postgres_user: postgres_user_{{ db.owner }}

{% if custom_psql in db %}
postgres_custom_psql_{{ db_name }}:
    cmd.run:
        - name: psql {{ db.name }} -c '{{ db.custom_psql }}'
        - runas: {{ user.name }}
        - require:
            - postgresql_database_{{ db_name }}
{% endif %}

{% endfor %}
