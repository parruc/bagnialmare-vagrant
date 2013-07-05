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
            - supervisor
    pip:
        - installed
        - names:
            - virtualenvwrapper

{% for venv_name, venv in pillar['venv'].venvs.iteritems() %}
venv_group_{{ venv_name }}:
    group.present:
        - name: {{ venv.group }}

venv_user_{{ venv_name }}:
    user.present:
        - name: {{ venv.user }}
        - password: {{ venv.pass }}
        - groups:
            - {{ venv.group }}
        - shell: /bin/bash
        - home: True
        - system: True
        - require:
            - group: venv_group_{{ venv_name }}

venv_{{ venv_name }}:
    virtualenv.managed:
        - name: {{ venv.path }}
        - no_site_packages: True
        - packages: {{ venv.packages }}
        - user: {{ venv.user }}
        - group: {{ venv.group }}
        - file_mode: 640
        - replace: True
    require:
        - pkg: venv_reqs
        - user: venv_user
{% endfor %}
