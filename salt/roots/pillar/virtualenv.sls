{% set dev = grains['configuration'] in ['local', 'dev'] %}
venv:
    venvs:
        ombrelloni:
            path: '/var/www/ombrelloni.it/venv'
            packages:
                - 'BeautifulSoup'
                - 'Django'
                - 'Jinja2'
                - 'MarkupSafe'
                - 'Pillow'
                - 'Pygments'
                - 'South'
                - 'Sphinx'
                - 'argparse'
                - 'django-autoslug'
                - 'django-allauth'
                - 'django-modeltranslation'
                - 'docutils'
                - 'whoosh'
                - 'lxml'
                - 'paramiko'
                - 'psycopg2'
                - 'pycrypto'
                - 'python-ptrace'
                - 'simplejson'
                - 'sorl-thumbnail'
                - 'uWSGI'
                - 'wsgiref'
                - 'Paste'
                - 'django_compressor'
                - 'cssmin'
                - 'jsmin'
                - 'geopy'
            {% if dev %}
                - 'factory-boy'
                - 'ipdb'
                - 'ipython'
                - 'django-debug-toolbar'
                - 'uwsgitop'
                - 'coverage'
            {% endif %}

{# KEEP FOR REFERENCE: TO ADD THIRD PARTY PACKAGES IN DEV MODE --editable=hg+https://bitbucket.org/mchaput/whoosh#egg=Whoosh #}
