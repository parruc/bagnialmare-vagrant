{% set dev = grains['configuration'] in ['dev'] %}

{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar.users[django_name] %}

add_dbutils_directory_{{ django_name }}:
    file.recurse:
        - name: {{ user.home_path }}/django/dbutils/
        - source: salt://cronjobs/dbutils
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 500
        - template: jinja
        - defaults:
            django_name: {{ django_name }}
            django_path: {{ django.path }}
        - makedirs: True
        - replace: True

{% if dev %}

add_cronjob_dumpdata{{ django_name }}:
    cron.present:
        - name: {{ user.home_path }}/django/dbutils/dumpdata.sh
        - user: {{ user.name }}
        - minute: 0
        - hour: 21
        - comment: Dump django data every day at 21 PM UTC 3:00 AM and commit+push the dump
        - require:
            - file: add_dbutils_directory_{{ django_name }}

add_cronjob_dumpdb{{ django_name }}:
    cron.present:
        - name: {{ user.home_path }}/django/dbutils/dumpdb.sh
        - user: root
        - minute: 0
        - hour: 20
        - comment: Dump django db every day at 20 PM UTC 2:00 AM and commit the dump
        - require:
            - file: add_dbutils_directory_{{ django_name }}

{% endif %}

{% endfor %}
