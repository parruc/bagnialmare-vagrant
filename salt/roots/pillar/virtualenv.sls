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
                - --editable=git+https://github.com/deschler/django-modeltranslation#egg=modeltranslation'
                - 'docutils==0.10'
                - 'whoosh==2.5.4'
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
                - 'django_compressor==1.3'
                - 'cssmin==0.1.4'
                - 'jsmin==2.0.4'
                - 'geopy==0.95.1'
            {% if dev %}
                - 'ipdb==0.7'
                - 'ipython==0.13.2'
                - 'django-debug-toolbar==0.9.4'
                - 'uwsgitop==0.6.2'
                - 'coverage==3.6'
            {% endif %}

{# KEEP FOR REFERENCE: TO ADD THIRD PARTY PACKAGES IN DEV MODE --editable=hg+https://bitbucket.org/mchaput/whoosh#egg=Whoosh #}