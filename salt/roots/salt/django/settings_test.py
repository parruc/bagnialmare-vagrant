#settings file for running tests
from settings import *

def remove_from_tuple(t, el):
    if el in t:
        index = t.index(el)
        return t[:index] + t[index + 1:]
    else:
        return t

{% set db = pillar['pg'].dbs['test_' + django_name] %}

DATABASES['default']['USER'] = '{{db.owner}}'
WHOOSH_INDEX = os.path.join(os.path.dirname(__file__), 'whoosh_index_test')

INSTALLED_APPS = remove_from_tuple(INSTALLED_APPS, 'debug_toolbar')
MIDDLEWARE_CLASSES = remove_from_tuple(MIDDLEWARE_CLASSES, 'debug_toolbar.middleware.DebugToolbarMiddleware')
