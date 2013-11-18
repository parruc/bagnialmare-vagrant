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
