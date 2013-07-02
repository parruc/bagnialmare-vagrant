nginx_reqs:
    pkg:
        - installed
        - names:
            - nginx

nginx_group:
    group.present:
        - name: {{ pillar['nginx'].group }}

nginx_user:
    user.present:
        - name: {{ pillar['nginx'].user }}
        - password: {{ pillar['nginx'].pass }}
        - groups:
            - {{ pillar['nginx'].group }}
        - shell: /bin/bash
        - home: False
        - system: True
        - require:
            - group: nginx_group

nginx_service:
    service.running:
        - name: nginx
        - enabled: True
        - require:
            - pkg: nginx_reqs
            - user: nginx_user
        - watch:
            - file: /etc/nginx/*

nginx_remove_default:
    file.absent:
        - name: /etc/nginx/sites-enabled/default
    require:
        - service: nginx_service

{% for host_name, host in pillar['nginx'].hosts.iteritems() %}
nginx_{{ host_name }}_error_log:
    file.touch:
        - name: {{ host.error_log }}
        - user: {{ pillar['nginx'].user }}
        - group: {{ pillar['nginx'].group }}
        - file_mode: 640
        - makedirs: True

nginx_{{ host_name }}_access_log:
    file.touch:
        - name: {{ host.access_log }}
        - user: {{ pillar['nginx'].user }}
        - group: {{ pillar['nginx'].group }}
        - file_mode: 640
        - makedirs: True

#TODO DA CREARE CON LO STESSO UTENTE DI DJANGO
{% if host.media %}
nginx_{{ host_name }}_media_dir:
    file.directory:
        - name: {{ host.media }}
        - user: {{ pillar['nginx'].user }}
        - group: {{ pillar['nginx'].group }}
        - mode: 755
        - makedirs: True
{% endif %}

#TODO DA CREARE CON LO STESSO UTENTE DI DJANGO
{% if host.static %}
nginx_{{ host_name }}_static_dir:
    file.directory:
        - name: {{ host.static }}
        - user: {{ pillar['nginx'].user }}
        - group: {{ pillar['nginx'].group }}
        - mode: 755
        - makedirs: True
{% endif %}

nginx_site_{{ host_name }}:
    file.managed:
        - name: /etc/nginx/sites-available/{{ host_name }}.vhost
        - source: salt://nginx/config/sites-available/{{ host_name }}.vhost
        - template: jinja
        - context:
            host: {{ host }}
            host_name: {{ host_name }}
        - user: root
        - group: root
        - file_mode: 644
        - replace: True
    require:
        - service: nginx_service

nginx_{{ host_name }}:
    file.symlink:
        - name: /etc/nginx/sites-enabled/{{ host_name }}.vhost
        - target: /etc/nginx/sites-available/{{ host_name }}.vhost
        - user: root
        - group: root
        - file_mode: 644
        - force: True
        - require:
            - file: nginx_site_{{ host_name }}
            - file: nginx_{{ host_name }}_error_log
            - file: nginx_{{ host_name }}_access_log
{% endfor %}
