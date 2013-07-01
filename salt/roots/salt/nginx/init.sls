nginx_reqs:
    pkg:
        - installed
        - names:
            - nginx
    service.running:
        - name: nginx
        - enabled: True
        - watch:
            - file: /etc/nginx/*

nginx_remove_default:
    file.absent:
        - name: /etc/nginx/sites-enabled/default

nginx_sites:
    file.recurse:
        - name: /etc/nginx/sites-available
        - source: salt://nginx/config/sites-available
        - user: root
        - group: root
        - file_mode: 644
    require:
        - pkg: nginx_reqs
        - pkg: nginx_remove_defaul

nginx_ombrelloni:
    file.symlink:
        - name: /etc/nginx/sites-available/{{ pillar["host"] }}
        - target: /etc/nginx/sites-enabled/{{ pillar["host"] }}
        - template: jinja
        - user: root
        - group: root
        - file_mode: 644
        - force: True
    require:
        - pkg: nginx_sites
