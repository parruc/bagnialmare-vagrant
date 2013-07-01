uwsgi_reqs:
    pip.installed:
        - name: uwsgi
    require:
        - pkg: python-dev
        - pkg: python-pip

uwsgi-service:
    service.running:
        - enable: True
        - name: uwsgi
        - watch:
            - file: /etc/init/uwsgi.conf
    require:
        - pkg: uwsgi_reqs


uwsgi_conf:
    file.managed:
        - name: /etc/init/uwsgi.conf
        - source: salt://uwsgi/uwsgi.conf
        - temlpate: jinja
    require:
        - pkg: uwsgi_reqs


uwsgi_log:
    file.managed:
        - name: /var/log/uwsgi.log
        - user: www-data
        - group: www-data
        - makedirs: true
    require:
        - pkg: uwsgi_reqs
        - pkg: nginx_reqs

app_log:
    file.managed:
        - name: /var/log/uwsgi/app.log
        - user: www-data
        - group: www-data
        - makedirs: true
    require:
        - pkg: uwsgi_reqs
        - pkg: nginx_reqs

emperor_log:
    file.managed:
        - name: /var/log/uwsgi/emperor.log
        - user: www-data
        - group: www-data
        - makedirs: true
    require:
        - pkg: uwsgi_reqs
        - pkg: nginx_reqs
