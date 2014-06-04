sup:
    sups:
        ombrelloni:
            name: 'ombrelloni'
            model: 'django.conf'
            target: '/etc/supervisor/conf.d/ombrelloni.conf'
            command: ''
        ombrelloni-offloader:
            name: 'ombrelloni'
            model: 'django-external-process.conf'
            target: '/etc/supervisor/conf.d/ombrelloni-offloader.conf'
            command: '/newsletters/mailoffloader.py'