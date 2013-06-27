postgres_dependecise:
    pkg:
        - installed
        - names:
            - postgresql-9.1
            - postgresql-server-dev-9.1
            - postgresql-contrib-9.1
            - postgresql-9.1-postgis
    service.running:
        - enabled: True
        - watch:
            - file: /etc/postgresql/9.1/main/pg_hba.conf

{{ pillar["dbuser"] }}:
    postgres_user:
        - present
        - user: {{ pillar["dbuser"] }}
        - password: {{ pillar["dbpassword"] }}
        - runas: postgres

{{ pillar["dbname"] }}
    postgres_database:
        - present
        - name: {{ pillar["dbname"] }}
        - encoding: UTF-8
        - runas: postgres
        - owner: {{ pillar["dbuser"] }}
