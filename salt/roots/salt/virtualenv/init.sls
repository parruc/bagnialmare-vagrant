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
        - names:
            - virtualenv
            - virtualenvwrapper
        - require:
            - pkg: venv_reqs



{% for venv_name, venv in pillar['venv'].venvs.iteritems() %}
{% set user = pillar['users'][venv_name] %}
venv_{{ venv_name }}:
    virtualenv.managed:
        - name: {{ venv.path }}
        - no_site_packages: True
        - python: python2.7
        - user: {{ user.name }}
        - require:
            - pkg: lib_reqs
            - pkg: venv_reqs
            - pip: venv_reqs
            - file: user_with_home_{{ venv_name }}

venv_pip_{{ venv_name }}:
    pip.installed:
        - names:
    {% for package in venv.packages %}
            - {{ package }}
    {% endfor %}
        - bin_env: {{ venv.path }}/bin/pip
        - timeout: 3
        - user: {{ user.name }}
        - require:
            - virtualenv: venv_{{ venv_name }}

{% endfor %}
