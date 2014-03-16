{% set dev = grains['configuration'] in ['dev'] %}

{% if dev %}

{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar.users[django_name] %}

add_cron_dumpdata_{{ django_name }}:
    file.managed:
        - name: {{ user.home_path }}/dbutils/dumpdata.sh
        - source: salt://cronjobs/dumpdata.sh
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 500
        - template: jinja
        - defaults:
            django_name: {{ django_name }}

add_cron_dumpdb_{{ django_name }}:
    file.managed:
        - name: {{ user.home_path }}/dbutils/dumpdb.sh
        - source: salt://cronjobs/dumpdb.sh
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 500
        - template: jinja
        - defaults:
            django_name: {{ django_name }}

add_cronjob_dumpdata{{ django_name }}:
    cron.present:
        - name: {{ user.home_path }}/dbutils/dumpdata.sh
        - user: {{ user.name }}
        - minute: 0
        - hour: 21
        - comment: Dump django data every day at 21 PM UTC 3:00 AM and commit+push the dump

add_cronjob_dumpdb{{ django_name }}:
    cron.present:
        - name: {{ user.home_path }}/dbutils/dumpdb.sh
        - user: root
        - minute: 0
        - hour: 20
        - comment: Dump django db every day at 20 PM UTC 2:00 AM and commit the dump

{% endfor %}
{% endif %}
