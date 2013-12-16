{% set loc = grains['configuration'] in ['local'] %}
base:
    '*':
        - django
        - git
        - lib
        - nginx
        - postgres
        - supervisor
        - users
        - uwsgi
        - virtualenv
        - cronjobs
        {% if loc %}
        - samba
        {% endif %}
