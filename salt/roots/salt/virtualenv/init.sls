venv_reqs:
    pkg:
        - installed
        - names:
            - python2.7
            - python2.7-dev
            - python-pip
            - python-virtualenv
            - mercurial #For pip checkout
            - git #For pip checkout
            - subversion #For pip checkout

{% for venv_name, venv in pillar['venv'].venvs.iteritems() %}
{% set user = pillar['users'][venv_name] %}
venv_{{ venv_name }}:
    virtualenv.managed:
        - name: {{ venv.path }}
        - no_site_packages: True
        - packages: {{ venv.packages }}
        - user: {{ user.name }}
        - group: {{ user.group }}
        - file_mode: 640
        - replace: True
    require:
        - pkg: venv_reqs
        - user: user_{{ venv_name }}
{% endfor %}
