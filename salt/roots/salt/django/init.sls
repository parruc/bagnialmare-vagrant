{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar['users'][django_name] %}

django_wsgi_{{ django_name }}:
    file.managed:
        - name: {{ django.path }}/{{ django_name }}/wsgi.py
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
        - require:
            - virtualenv: venv_{{ django_name }}
            - user: user_with_home_{{ django_name }}

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
        - require:
            - virtualenv: venv_{{ django_name }}
            - user: user_with_home_{{ django_name }}

{% endfor %}

