{% set dev = grains['configuration'] in ['local', 'dev'] %}
django:
    djangos:
        ombrelloni:
            settings: 'ombrelloni.settings'
            path: '/var/www/ombrelloni.it/django'
            db_engine: 'django.contrib.gis.db.backends.postgis'
            db_host: 'localhost'
            db_port: '5432'
        {% if dev %}
            debug: 'True'
        {% else %}
            debug: 'False'
        {% endif %}
            installed_apps:
                - 'django.contrib.auth'
                - 'django.contrib.contenttypes'
                - 'django.contrib.sessions'
                - 'django.contrib.messages'
                - 'django.contrib.staticfiles'
                - 'django.contrib.admin'
                - 'django.contrib.admindocs'
                - 'django.contrib.gis'
                - 'south'
                - 'autoslug'
                - 'sorl.thumbnail'
                - 'compressor'
                - 'bagni'
        {% if dev %}
                - 'fts'
                - 'debug_toolbar'
        {% endif %}
            secret_key: 'u)-#(7qe0o9=+ez%ay0=vi#oc52*&4np3x5^m!!c6u$@yr5eud'
            middleware:
                - 'django.contrib.sessions.middleware.SessionMiddleware'
                - 'django.middleware.locale.LocaleMiddleware'
                - 'django.middleware.common.CommonMiddleware'
                - 'django.middleware.csrf.CsrfViewMiddleware'
                - 'django.contrib.auth.middleware.AuthenticationMiddleware'
                - 'django.contrib.messages.middleware.MessageMiddleware'
        {% if dev %}
                - 'debug_toolbar.middleware.DebugToolbarMiddleware'
        {% endif %}
            template_loaders:
                - 'django.template.loaders.filesystem.Loader'
                - 'django.template.loaders.app_directories.Loader'
            staticfiles_finders:
                - 'django.contrib.staticfiles.finders.FileSystemFinder'
                - 'django.contrib.staticfiles.finders.AppDirectoriesFinder'
                - 'compressor.finders.CompressorFinder'
            staticfiles_dirs:
                - 'static'
            fixture_dirs:
                - 'fixtures'
            template_dirs:
                - 'templates'
            template_context_processors:
                - 'django.core.context_processors.request'
                - 'django.contrib.auth.context_processors.auth'
                - 'django.core.context_processors.debug'
                - 'django.core.context_processors.i18n'
                - 'django.core.context_processors.media'
                - 'django.core.context_processors.static'
                - 'django.core.context_processors.tz'
                - 'django.contrib.messages.context_processors.messages'
