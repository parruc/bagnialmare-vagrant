{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar['users'][django_name] %}
{% set tester = pillar['users']["test_" + django_name] %}
{% set host = pillar['nginx'].hosts[django_name] %}
{% set db = pillar['pg'].dbs[django_name] %}
{% set test_db = pillar['pg'].dbs["test_" + django_name] %}
{% set venv = pillar['venv'].venvs[django_name] %}

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
            - file: user_with_home_{{ django_name }}
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
            - file: user_with_home_{{ django_name }}

django_settings_test_{{ django_name }}:
    file.managed:
        - name: {{ django.path }}/{{ django_name }}/settings_test.py
        - source: salt://django/settings_test.py
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 644
        - makedirs: True
        - replace: True
        - template: jinja
        - context:
            db: {{ test_db }}
        - require:
            - virtualenv: venv_{{ django_name }}
            - file: user_with_home_{{ django_name }}

django_logs_{{ django_name }}:
    file.managed:
        - name: {{ host.root }}/log/django.log
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - replace: True
        - require:
            - file: user_with_home_{{ django_name }}

django_loaddata_script_{{ django_name }}:
    file.managed:
        - source: salt://django/prepare_data.sh
        - name: /tmp/prepare_data.sh
        - mode: 700
        - user: {{ user.name }}
        - group: {{ user.group }}
        - makedirs: True
        - replace: True
        - template: jinja
        - context:
            django: {{ django }}
            django_name: {{ django_name }}
            venv: {{ venv }}
        - require:
            - file: user_with_home_{{ django_name }}
            - virtualenv: venv_{{ django_name }}
            - git: git_{{ django_name }}

django_loaddata_{{ django_name }}:
    cmd.run:
        - name: /tmp/prepare_data.sh
        #- unless:
        - user: {{ user.name }}
        - cwd: {{ django.path }}
        - group: {{ user.group }}
        - require:
            - file: django_settings_{{ django_name }}
            - file: django_settings_test_{{ django_name }}
            - file: nginx_{{ django_name }}_static_dir
            - file: django_loaddata_script_{{ django_name }}

{% if django.coverage_command and django.coverage_path %}
django_coverage_{{ django_name }}:
    cmd.run:
        - name: {{ django.coverage_command }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - cwd: {{ django.path }}
        - require:
            - git: git_{{ django_name }}
            - file: django_settings_{{ django_name }}
            - pip: venv_pip_{{ django_name }}
{% endif %}

{% if django.doc_command and django.doc_path %}
django_doc_{{ django_name }}:
    cmd.run:
        - name: {{ django.doc_command }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - cwd: {{ django.path }}/doc
        - require:
            - git: git_{{ django_name }}
            - file: django_settings_{{ django_name }}
{% endif %}

{% endfor %}

