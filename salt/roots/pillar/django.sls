django:
    djangos:
        ombrelloni:
            settings: 'settings'
            path: '/home/ombrelloni/django'
            db_engine: 'django.contrib.gis.db.backends.postgis'
            db_host: 'localhost'
            db_port: '5432'
            debug: 'True'
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
                - 'haystack'
                - 'bagni'
            secret_key: 'u)-#(7qe0o9=+ez%ay0=vi#oc52*&4np3x5^m!!c6u$@yr5eud'
            middleware:
                - 'django.middleware.common.CommonMiddleware'
                - 'django.contrib.sessions.middleware.SessionMiddleware'
                - 'django.middleware.csrf.CsrfViewMiddleware'
                - 'django.contrib.auth.middleware.AuthenticationMiddleware'
                - 'django.contrib.messages.middleware.MessageMiddleware'
            template_loaders:
                - 'django.template.loaders.filesystem.Loader'
                - 'django.template.loaders.app_directories.Loader'
            staticfiles_finders:
                - 'django.contrib.staticfiles.finders.FileSystemFinder'
                - 'django.contrib.staticfiles.finders.AppDirectoriesFinder'
            staticfiles_dirs: []


