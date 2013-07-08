sup_reqs:
    pkg:
        - installed
        - names:
            - supervisor

sup_service:
    service.running:
        - name: supervisord
        - watch:
            - file: /etc/supervisor/*
        - require:
            - pkg: sup_reqs

{% for sup_name, sup in pillar['sup'].sups.iteritems() %}

sup_conf_{{ sup_name }}:
    file.managed:
        - name: /etc/supervisor/conf.d/{{ sup_name }}.conf
        - source: salt://supervisor/supervisor.conf
        - template: jinja
        - context:
            sup: {{ sup }}
            sup_name: {{ sup_name }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - require:
            - pkg: sup_reqs

sup_service_{{ sup_name }}:
    supervisord.running:
        - name: {{ sup_name }}
        - conf_file: /etc/supervisor/conf.d/{{ sup_name }}.conf
        - watch:
            - file: uwsgi_conf_{{ sup_name }}
        - require:
            - service: sup_service
            - file: sup_conf_{{ sup_name }}
            - file: uwsgi_logs_{{ sup_name }}

{% endfor %}

