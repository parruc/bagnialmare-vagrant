sup_reqs:
    pkg:
        - installed
        - names:
            - supervisor

sup_service:
    service.running:
        - name: supervisor
        - sig: supervisord
        - watch:
            - file: /etc/supervisor/*
        - require:
            - pkg: sup_reqs

{% for sup_name, sup in pillar['sup'].sups.iteritems() %}
{% set host = pillar['nginx'].hosts[sup_name] %}
{% set user = pillar['users'][sup_name] %}

sup_conf_{{ sup_name }}:
    file.managed:
        - name: {{ sup.conf }}
        - source: salt://supervisor/{{ sup.model }}
        - user: root
        - group: root
        - template: jinja
        - defaults:
            sup_name: {{ sup.name }}
            sup_command: {{ sup.command }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - require:
            - pkg: sup_reqs

sup_service_{{ sup_name }}:
    supervisord.running:
        - name: {{ sup_name }}
        - watch:
            - file: uwsgi_conf_{{ sup_name }}
        - require:
            - service: sup_service
            - file: sup_conf_{{ sup_name }}
            - file: sup_logs_{{ sup_name }}
            - git: git_{{ sup_name }}

sup_logs_{{ sup_name }}:
    file.managed:
        - name: {{ host.root }}/log/supervisor.log
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - replace: True
        - require:
            - file: user_with_home_{{ sup.name }}

{% endfor %}