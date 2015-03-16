{% set dev = grains['configuration'] in ['local', 'dev'] %}
venv:
    venvs:
        ombrelloni:
            path: '/var/www/ombrelloni.it/venv'
            packages:
                - 'BeautifulSoup'
                - 'Django>1.6,<1.7'
                - 'python-memcached'
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
                - 'django-ckeditor-updated'
                - 'pyzmq'
            {% if dev %}
                - 'factory-boy'
                - 'ipdb'
                - 'ipython'
                - 'django-debug-toolbar'
                - 'django-debug-toolbar-line-profiler'
                - 'uwsgitop'
                - 'coverage'
                - 'selenium'
            {% else %}
                - 'opbeat'
            {% endif %}

{# KEEP FOR REFERENCE: TO ADD THIRD PARTY PACKAGES IN DEV MODE --editable=hg+https://bitbucket.org/mchaput/whoosh#egg=Whoosh #}
{#                - 'django-dtpanel-htmltidy' #}
