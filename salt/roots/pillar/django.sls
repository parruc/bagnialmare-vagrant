{% set dev = grains['configuration'] in ['local', 'dev'] %}
django:
    djangos:
        ombrelloni:
            settings: 'ombrelloni.settings'
            path: '/var/www/ombrelloni.it/django'
            logs_path: '/var/www/ombrelloni.it/log'
            db_engine: 'django.contrib.gis.db.backends.postgis'
            db_host: 'localhost'
            db_port: '5432'
            email_host: 'mail.bagnialmare.com'
            email_port: '25'
            email_user: 'info@bagnialmare.com'
            email_pass: 'fTIm9sr2@thx'
        {% if dev %}
            debug: 'True'
            coverage_command: './unittests'
            doc_command: 'make html'
            coverage_path: '/var/www/ombrelloni.it/django/htmlcov'
            doc_path: '/var/www/ombrelloni.it/django/doc/_build/html'
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
                - 'django.contrib.sites'
                - 'django.contrib.sitemaps'
                - 'allauth'
                - 'allauth.account'
                - 'allauth.socialaccount'
                {#
                - 'allauth.socialaccount.providers.facebook'
                - 'allauth.socialaccount.providers.google'
                - 'allauth.socialaccount.providers.openid'
                - 'allauth.socialaccount.providers.twitter'
                #}
                - 'modeltranslation'
                - 'south'
                - 'autoslug'
                - 'sorl.thumbnail'
                - 'compressor'
                - 'bagni'
                - 'newsletters'
                - 'multilingual'
                - 'authauth'
                - 'contacts'
                - 'userfeedback'
                - 'ckeditor'
        {% if dev %}
                - 'fts'
                - 'debug_toolbar'
{#                - 'debug_toolbar_htmltidy' #}
                - 'debug_toolbar_line_profiler'
        {% endif %}
            secret_key: 'u)-#(7qe0o9=+ez%ay0=vi#oc52*&4np3x5^m!!c6u$@yr5eud'
            middleware:
                - 'django.middleware.gzip.GZipMiddleware'
                - 'django.contrib.sessions.middleware.SessionMiddleware'
                - 'django.middleware.locale.LocaleMiddleware'
                - 'django.middleware.common.CommonMiddleware'
                - 'django.middleware.csrf.CsrfViewMiddleware'
                - 'django.contrib.auth.middleware.AuthenticationMiddleware'
                - 'django.contrib.messages.middleware.MessageMiddleware'
        {% if dev %}
                - 'debug_toolbar.middleware.DebugToolbarMiddleware'
        {% endif %}
            authentication_backends:
                - 'django.contrib.auth.backends.ModelBackend'
                - 'allauth.account.auth_backends.AuthenticationBackend'
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
                - 'allauth.account.context_processors.account'
                - 'allauth.socialaccount.context_processors.socialaccount'
                - 'django.core.context_processors.debug'
                - 'django.core.context_processors.i18n'
                - 'django.core.context_processors.media'
                - 'django.core.context_processors.static'
                - 'django.core.context_processors.tz'
                - 'django.contrib.messages.context_processors.messages'
            locale_paths:
                - '/var/www/ombrelloni.it/django/ombrelloni/locale/'
                - '/var/www/ombrelloni.it/django/authauth/locale/'
                - '/var/www/ombrelloni.it/django/bagni/locale/'
                - '/var/www/ombrelloni.it/django/contacts/locale/'

