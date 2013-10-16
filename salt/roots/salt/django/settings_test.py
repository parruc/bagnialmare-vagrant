#settings file for running tests
from settings import *

{% set db = pillar['pg'].dbs['test_' + django_name] %}

DATABASES['default']['USER'] = '{{db.owner}}'
