{% for uwsgi_name, uwsgi in pillar['uwsgi'].uwsgis.iteritems() %}
uwsgi_group_{{ uwsgi_name }}:
    group.present:
        - name: {{ uwsgi.group }}

uwsgi_user_{{ uwsgi_name }}:
    user.present:
        - name: {{ uwsgi.user }}
        - password: {{ uwsgi.pass }}
        - groups:
            - {{ uwsgi.group }}
        - shell: /bin/bash
        - home: True
        - system: True
        - require:
            - group: uwsgi_group_{{ uwsgi_name }}

uwsgi_conf_{{ uwsgi_name }}:
    file.managed:
        - name: {{ uwsgi.django_path }}/uwsgi.ini
        - source: salt://uwsgi/uwsgi.ini
        - user: {{ venv.user }}
        - group: {{ venv.group }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - temlpate: jinja
        - context:
            uwsgi_name: {{ uwsgi_name }}
            uwsgi: {{ uwsgi }}
    require:
        - pkg: uwsgi_reqs
        - user: uwsgi_user_{{ uwsgi_name }}

uwsgi_supervisor_conf_{{ uwsgi_name }}:
    file.managed:
        - name: /etc/supervisor/conf.d/{{ uwsgi_name }}.conf
        - source: salt://uwsgi/supervisor.conf
        - user: root
        - group: root
        - file_mode: 640
        - replace: True
        - makedirs: True
        - temlpate: jinja
        - context:
            uwsgi_name: {{ uwsgi_name }}
            uwsgi: {{ uwsgi }}
    require:
        - pkg: uwsgi_reqs
        - user: uwsgi_user_{{ uwsgi_name }}

uwsgi_logs_{{ uwsgi_name }}:
    file.managed:
        - name: {{ uwsgi.home_path }}/log/uwsgi.log
        - user: {{ venv.user }}
        - group: {{ venv.group }}
        - replace: True
        - makedirs: True
        - file_mode: 640

uwsgi_supervisor_{{ uwsgi_name }}:
    supervisord:
        - running
        - watch:
            - file: uwsgi_supervisor_conf_{{ uwsgi_name }}
            - file: uwsgi_conf_{{ uwsgi_name }}
        - require:
            - file:
                uwsgi_logs_{{ uwsgi_name }}
{% endfor %}
