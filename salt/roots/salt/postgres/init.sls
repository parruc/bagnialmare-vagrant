postgres_reqs:
    pkg:
        - installed
        - names:
            - postgresql-9.1
            - postgresql-server-dev-9.1
            - postgresql-contrib-9.1
            - postgresql-9.1-postgis
    service.running:
        - name: postgresql
        - enabled: True
        - watch:
            - file: /etc/postgresql/9.1/main/pg_hba.conf

postgres_ombrelloni_user:
    postgres_user.present:
        - name: {{ pillar["dbuser"] }}
        - password: {{ pillar["dbpassword"] }}
        - runas: postgres
    require:
        - pkg: postgres_reqs

postgres_ombrelloni_db:
    postgres_database.present:
        - name: {{ pillar["dbname"] }}
        - template: template0
        - encoding: UTF-8
        - runas: postgres
        - owner: {{ pillar["dbuser"] }}
    require:
        - pkg: postgres_ombrelloni_user
