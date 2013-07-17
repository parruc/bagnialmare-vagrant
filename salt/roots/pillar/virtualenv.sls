{% set dev = grains['configuration'] in ['local', 'dev'] %}
venv:
    venvs:
        ombrelloni:
            path: '/var/www/ombrelloni.it/venv'
            packages:
                - 'BeautifulSoup==3.2.1'
                - 'Django==1.5.1'
                - 'Jinja2==2.7'
                - 'MarkupSafe==0.18'
                - 'Pillow==2.0.0'
                - 'Pygments==1.6'
                - 'South==0.8.1'
                - 'Sphinx==1.2b1'
                - 'argparse==1.2.1'
                - 'django-autoslug==1.6.1'
                - 'docutils==0.10'
                - 'hg+https://bitbucket.org/mchaput/whoosh@00a347c#egg=Whoosh'
                - 'git+https://github.com/parruc/django-haystack.git#egg=django-haystack'
                - 'ipdb==0.7'
                - 'ipython==0.13.2'
                - 'lxml==3.2.1'
                - 'paramiko==1.10.1'
                - 'psycopg2==2.5'
                - 'pycrypto==2.6'
                - 'python-ptrace==0.6.5'
                - 'simplejson==3.3.0'
                - 'sorl-thumbnail==11.12'
                - 'uWSGI==1.9.13'
                - 'wsgiref==0.1.2'
                - 'Paste==1.7.5.1'
            {% if dev %}
                - django-debug-toolbar
                - uwsgitop
            {% endif %}
