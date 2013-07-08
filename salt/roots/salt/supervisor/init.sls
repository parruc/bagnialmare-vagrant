{% for sup_name, sup in pillar['sup'].sups.iteritems() %}
{% set user = pillar['users'][sup_name] %}

sup_reqs_{{ sup_name }}:
    pip.installed:
        - name: supervisor
        - bin_env: {{ sup.venv_path }}/bin/pip

sup_conf_{{ sup_name }}:
    file.managed:
        - name: {{ sup.venv_path }}/{{ sup_name }}.conf
        - source: salt://supervisor/supervisor.conf
        - temlpate: jinja
        - context:
            sup: {{ sup }}
            sup_name: {{ sup_name }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - require:
            - pip: sup_reqs_{{ sup_name }}

sup_service_{{ sup_name }}:
    supervisord.running:
        - name: {{ sup_name }}
        - bin_env: {{ sup.venv_path }}
        - conf_file: {{ sup.venv_path }}/{{ sup_name }}.conf
        - runas: {{ user.name }}
        - watch:
            - file: sup_conf_{{ sup_name }}
            - file: uwsgi_conf_{{ sup_name }}
        - require:
            - file: uwsgi_logs_{{ sup_name }}
            - pip: uwsgi_reqs


{% endfor %}
