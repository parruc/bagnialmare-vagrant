{% for sup_name, sup in pillar['sup'].sups.iteritems() %}
sup_reqs:
    pkg:
        - installed
        - names:
            - supervisor

sup_conf_{{ sup_name }}:
    file.managed:
        - name: /etc/supervisor/conf.d/{{ sup_name }}.conf
        - source: salt://supervisor/supervisor.conf
        - temlpate: jinja
        - context:
            sup: {{ sup }}
            sup_name: {{ sup_name }}
        - user: root
        - group: root
        - file_mode: 640
        - replace: True
        - makedirs: True
        - require:
            - pkg: sup_reqs

sup_service{{ sup_name }}:
    service.running:
        - name: supervisor
        - watch:
            - file: sup_conf_{{ sup_name }}
            - file: uwsgi_conf_{{ sup_name }}
        - require:
            - file: uwsgi_logs_{{ sup_name }}
            - pip: uwsgi_reqs
{% endfor %}
