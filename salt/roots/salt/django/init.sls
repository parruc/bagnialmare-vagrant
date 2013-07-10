{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar['users'][django_name] %}
{% set host = pillar['nginx'].hosts[django_name] %}
{% set db = pillar['pg'].dbs[django_name] %}

django_wsgi_{{ django_name }}:
    file.managed:
        - name: {{ django.path }}/wsgi.py
        - source: salt://django/wsgi.py
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 644
        - makedirs: True
        - replace: True
        - template: jinja
        - context:
            django: {{ django }}
            django_name: {{ django_name }}
            host: {{ host }}
        - require:
            - virtualenv: venv_{{ django_name }}
            - user: user_with_home_{{ django_name }}
            - file: django_logs_{{ django_name }}

django_settings_{{ django_name }}:
    file.managed:
        - name: {{ django.path }}/{{ django_name }}/settings.py
        - source: salt://django/settings.py
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 644
        - makedirs: True
        - replace: True
        - template: jinja
        - context:
            django: {{ django }}
            django_name: {{ django_name }}
            db: {{ db }}
            host: {{ host }}
        - require:
            - virtualenv: venv_{{ django_name }}
            - user: user_with_home_{{ django_name }}

django_logs_{{ django_name }}:
    file.managed:
        - name: {{ host.root }}/log/django.log
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - replace: True
        - require:
            - user: user_with_home_{{ django_name }}

{% endfor %}

