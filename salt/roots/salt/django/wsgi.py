import os
import sys

{% set django = pillar['django'].djangos[django_name] %}
{% set host = pillar['nginx'].hosts[django_name] %}

sys.stdout = sys.stderr
sys.path.append('{{ django.path}}/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ django.settings }}")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from paste.exceptions.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application, debug={{ django.debug }}, error_log='{{ host.root }}/log/uwsgi/django.log')
