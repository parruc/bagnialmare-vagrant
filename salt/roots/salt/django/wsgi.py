import os
import sys

sys.stdout = sys.stderr
sys.path.append('{{ django.path}}/{{ django_name }}')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ django.settings }}")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from paste.exceptions.errormiddleware import ErrorMiddleware
application = ErrorMiddleware(application)
