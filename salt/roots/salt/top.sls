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
        {% if loc %}
        - samba
        {% endif %}
