{% set dev = grains['configuration'] in ['dev'] %}

{% if dev %}

{% for django_name, django in pillar['django'].djangos.iteritems() %}
{% set user = pillar.users[django_name] %}

add_cron_file_{{ django_name }}:
    file.managed:
        - name: {{ user.home_path }}/dbutils/dumpdata.sh
        - source: salt://cronjobs/dumpdata.sh
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 500
        - template: jinja
        - defaults:
            django_name: {{ django_name }}

add_cronjob_{{ django_name }}:
    cron.present:
        - name: {{ user.home_path }}/dbutils/dumpdata.sh
        - user: {{ user.name }}
        - minute: 0
        - hour: 21
        - comment: Dump django data every day at 21 PM UTC 3:00 AM and commit+push the dump

{% endfor %}
{% endif %}
