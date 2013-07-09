nginx_reqs:
    pkg:
        - installed
        - names:
            - nginx

nginx_service:
    service.running:
        - name: nginx
        - enabled: True
        - require:
            - pkg: nginx_reqs
            - user: user_nginx
        - watch:
            - file: /etc/nginx/*

nginx_remove_default:
    file.absent:
        - name: /etc/nginx/sites-enabled/default

{% for host_name, host in pillar['nginx'].hosts.iteritems() %}
{% set user = pillar['users'][host_name] %}

nginx_{{ host_name }}_error_pages:
    file.recurse:
        - name: {{ host.error_pages }}
        - source: salt://nginx/error
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - dir_mode: 755
        - template: jinja
        - context:
            host: {{ host }}
        - makedirs: True
        - require:
            - user: user_with_home_{{ host_name }}

nginx_{{ host_name }}_error_log:
    file.managed:
        - name: {{ host.error_log }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - require:
            - user: user_with_home_{{ host_name }}

nginx_{{ host_name }}_access_log:
    file.managed:
        - name: {{ host.access_log }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - makedirs: True
        - require:
            - user: user_with_home_{{ host_name }}

{% if host.media %}
nginx_{{ host_name }}_media_dir:
    file.directory:
        - name: {{ host.media }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 755
        - makedirs: True
        - require:
            - user: user_with_home_{{ host_name }}
            - pkg: nginx_reqs
{% endif %}

{% if host.static %}
nginx_{{ host_name }}_static_dir:
    file.directory:
        - name: {{ host.static }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - mode: 755
        - makedirs: True
        - require:
            - user: user_with_home_{{ host_name }}
            - pkg: nginx_reqs
{% endif %}

nginx_site_{{ host_name }}:
    file.managed:
        - name: /etc/nginx/sites-available/{{ host_name }}.vhost
        - source: salt://nginx/config/sites-available/host.vhost
        - template: jinja
        - context:
            host: {{ host }}
            host_name: {{ host_name }}
        - user: root
        - group: root
        - file_mode: 644
        - makedirs: True
        - replace: True
        - require:
            - pkg: nginx_reqs

nginx_{{ host_name }}:
    file.symlink:
        - name: /etc/nginx/sites-enabled/{{ host_name }}.vhost
        - target: /etc/nginx/sites-available/{{ host_name }}.vhost
        - user: root
        - group: root
        - file_mode: 644
        - force: True
        - makedirs: True
        - require:
            - pkg: nginx_reqs
            - file: nginx_site_{{ host_name }}
            - file: nginx_{{ host_name }}_error_log
            - file: nginx_{{ host_name }}_access_log
{% endfor %}
