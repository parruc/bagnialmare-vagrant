#settings file for running tests
from settings import *

DATABASES['default']['USER'] = '{{db.owner}}'
