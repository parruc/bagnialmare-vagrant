{% for uwsgi_name, uwsgi in pillar['uwsgi'].uwsgis.iteritems() %}
{% set host = pillar['nginx']['hosts'][uwsgi_name] %}
{% set user = pillar['users'][uwsgi_name] %}


uwsgi_reqs:
    pip.installed:
        - name: uwsgi
        - bin_env: {{ uwsgi.venv_path }}/bin/pip
        - require:
            - virtualenv: venv_{{ uwsgi_name }}

uwsgi_conf_{{ uwsgi_name }}:
    file.managed:
        - name: {{ uwsgi.django_path }}/uwsgi.ini
        - source: salt://uwsgi/uwsgi.ini
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - replace: True
        - makedirs: True
        - template: jinja
        - context:
            uwsgi_name: {{ uwsgi_name }}
            uwsgi: {{ uwsgi }}
            user: {{ user }}
            host: {{ host }}
        - require:
            - git: git_{{ uwsgi_name }}
            - user: user_with_home_{{ uwsgi_name }}
            - file: uwsgi_logs_{{ uwsgi_name }}

uwsgi_logs_{{ uwsgi_name }}:
    file.managed:
        - name: {{ host.root }}/log/uwsgi.log
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - replace: True
        - require:
            - user: user_with_home_{{ uwsgi_name }}


{% endfor %}
