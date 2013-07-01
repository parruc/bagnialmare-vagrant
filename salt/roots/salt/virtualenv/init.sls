virtualenv_req:
    pkg:
        - installed
        - names:
            - python-virtualenv
            - python-pip
    pip:
        - installed
        - names:
            - virtualenvwrapper

virtualenv_ombrelloni:
    virtualenv.managed:
        - name: {{ pillar["django_path"] }}/venv
        - no_site_packages: True
        - requirements: salt://virtualenv/ombrelloni_requirements.txt
    require:
        - pkg: lib_reqs
        - pkg: virtualenv_req
        - pkg: postgres_ombrelloni_db
        - pkg: python_reqs
        - pkg: git_ombrelloni
        - pkg: nginx_ombrelloni
