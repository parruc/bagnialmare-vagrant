# Django settings for ombrelloni project.

{% set django = pillar['django'].djangos[django_name] %}
{% set host = pillar['nginx'].hosts[django_name] %}
{% set db = pillar['pg'].dbs[django_name] %}
{% set dev = grains['configuration'] in ['local', 'dev'] %}
{% set loc = grains['configuration'] in ['local'] %}

import os

DEBUG = {{ django.debug }}
TEMPLATE_DEBUG = {{ django.debug }}
COMPRESS_ENABLED = not DEBUG

{% if django.debug %}
def show_toolbar(request):
    if request.GET.get("toolbar", None):
        return DEBUG
    return False
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'ombrelloni.settings.show_toolbar'
}
DEBUG_TOOLBAR_PATCH_SETTINGS = False
{% endif %}

ACCOUNT_SIGNUP_FORM_CLASS = "authauth.forms.ManagerSignupForm"
LOGIN_REDIRECT_URL = "homepage"

ADMINS = (
    ("Matteo Parrucci", "parruc@gmail.com", ),
    ("Nicola Valentini", "nicola.valentini@gmail.com", ),
    ("Marco Bartolini", "marcobartolini@gmail.com", ),
    ("Marco Benvenuto", "marco.benvenuto1@gmail.com", ),
)

MANAGERS = ADMINS

WHOOSH_INDEX = os.path.join(os.path.dirname(__file__), 'whoosh_index')

DATABASES = {
    'default': {
        'ENGINE': '{{ django.db_engine }}',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{ db.name }}',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '{{ db.owner }}',
        'PASSWORD': '{{ db.pass }}',
        'HOST': '{{ django.db_host }}',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '{{ django.db_port }}',                      # Set to empty string for default.
    },
}

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en' #default lnguage?!?

MODELTRANSLATION_AUTO_POPULATE = 'all'

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('it', gettext('Italiano')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '{{ host.media }}'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '{{ host.static }}'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    {% for staticfiles_dir in django.staticfiles_dirs %}os.path.join(os.path.dirname(__file__), '{{ staticfiles_dir }}'),
    {% endfor %}
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    {% for staticfiles_finder in django.staticfiles_finders %}'{{ staticfiles_finder }}',
    {% endfor %}
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{ django.secret_key }}'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    {% for template_loader in django.template_loaders %}'{{ template_loader }}',
    {% endfor %}
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    {% for middleware in django.middleware %}'{{ middleware }}',
    {% endfor %}
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    {% for authentication_backend in django.authentication_backends %}'{{ authentication_backend }}',
    {% endfor %}
)

FIXTURE_DIRS = (
    {% for fixture_dir in django.fixture_dirs %}os.path.join(os.path.dirname(__file__), '{{ fixture_dir }}'),
    {% endfor %}
)

TEMPLATE_CONTEXT_PROCESSORS = (
    {% for template_context_processor in django.template_context_processors %}'{{ template_context_processor }}',
    {% endfor %}
)

ROOT_URLCONF = '{{ django_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ django_name }}.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    {% for template_dir in django.template_dirs %}
        os.path.join(os.path.dirname(__file__), '{{ template_dir }}'),
    {% endfor %}
)

LOCALE_PATHS = (
    {% for locale_path in django.locale_paths %}
        '{{ locale_path }}',
    {% endfor %}
)

INSTALLED_APPS = (
    {% for installed_app in django.installed_apps %}
        '{{ installed_app }}',
    {% endfor %}
)

# South specific configuration to exclude migrations from tests
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

{% if loc %}
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '../log/mail.log'
{% else %}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{{ django.email_host }}'
EMAIL_PORT = '{{ django.email_port }}'
EMAIL_HOST_USER = '{{ django.email_user }}'
EMAIL_HOST_PASSWORD = '{{ django.email_pass }}'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
{% endif %}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'bagni.console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
