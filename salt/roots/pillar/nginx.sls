nginx:
    hosts:
        ombrelloni:
            server_name : 'ombrelloni.it'
            root: '/var/www/ombrelloni.it'
            web: '/var/www/ombrelloni.it/web'
            error_log: '/var/www/ombrelloni.it/log/error.log'
            access_log: '/var/www/ombrelloni.it/log/access.log'
            error_pages: '/var/www/ombrelloni.it/web/error'
            analitycs_id: ''
            media: '/var/www/ombrelloni.it/web/media'
            static: '/var/www/ombrelloni.it/web/static'
