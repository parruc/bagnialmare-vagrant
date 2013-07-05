postgres_reqs:
    pkg:
        - installed
        - names:
            - postgresql-9.1
            - postgresql-server-dev-9.1
            - postgresql-contrib-9.1
            - postgresql-9.1-postgis

postgres_group:
    group.present:
        - name: {{ pillar['pg'].group }}

postgres_user:
    user.present:
        - name: {{ pillar['pg'].user }}
        - password: {{ pillar['pg'].pass }}
        - groups:
            - {{ pillar['pg'].group }}
        - shell: /bin/bash
        - home: False
        - system: True
        - require:
            - group: postgres_group

postgres_service:
    service.running:
        - name: postgresql
        - enable: True
        - reload: True
        - require:
            - user: postgres_user
            - pkg: postgres_reqs
        - watch:
            - file: postgresql_conf
            - file: pg_hba_conf

postgresql_conf:
    file.managed:
        - source: salt://postgres/postgresql.conf
        - name: /etc/postgresql/9.1/main/postgresql.conf
        - template: jinja
        - user: {{ pillar['pg'].user }}
        - group: {{ pillar['pg'].group }}
        - mode: 644
        - require:
            - user: postgres_user
            - pkg: postgres_reqs

pg_hba_conf:
    file.managed:
        - source: salt://postgres/pg_hba.conf
        - name: /etc/postgresql/9.1/main/pg_hba.conf
        - template: jinja
        - user: {{ pillar['pg'].user }}
        - group: {{ pillar['pg'].group }}
        - mode: 644
        - require:
            - user: postgres_user
            - pkg: postgres_reqs

{% for db_name, db in pillar['pg'].dbs.iteritems() %}
postgres_user_{{ db.owner }}:
    postgres_user.present:
        - name: {{ db.owner }}
        - password: {{ db.password }}
        - runas: {{ pillar['pg'].user }}
        - require:
            - user: postgres_user
            - service: postgres_service

postgresql_database_{{ db_name }}:
    postgres_database.present:
        - name: {{ db_name }}
        - owner: {{ db.owner }}
        - template: template0
        - runas: {{ pillar['pg'].user }}
        - require:
            - postgres_user: postgres_user_{{ db.owner }}

{% if custom_psql in db %}
postgres_custom_psql_{{ db_name }}:
    cmd.run:
        - name: psql {{ db_name }} -c '{{ db.custom_psql }}'
        - runas: {{ pillar['pg'].user }}
        - require:
            - postgresql_database_{{ db_name }}
{% endif %}

{% endfor %}
