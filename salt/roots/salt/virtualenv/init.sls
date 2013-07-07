venv_reqs:
    pkg:
        - installed
        - names:
            - python2.7
            - python2.7-dev
            - python-pip
            - mercurial #For pip checkout
            - git #For pip checkout
            - subversion #For pip checkout
    pip.installed:
        - name: virtualenv
        - require:
            - pkg: venv_reqs



{% for venv_name, venv in pillar['venv'].venvs.iteritems() %}
{% set user = pillar['users'][venv_name] %}
venv_{{ venv_name }}:
    virtualenv.managed:
        - name: {{ venv.path }}
        - no_site_packages: True
        - packages: {{ venv.packages }}
        - python: python2.7
        - runas: {{ user.name }}
        - require:
            - pkg: venv_reqs
            - pip: venv_reqs
            - user: user_{{ venv_name }}
{% endfor %}
