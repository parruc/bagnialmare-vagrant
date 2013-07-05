nginx:
    user: 'www-data'
    group: 'www-data'
    pass: '31xV#GHw7xH"vOov=Aer0fhJ7p5ojB'
    hosts:
        ombrelloni:
            server_name : 'ombrelloni.it'
            root : '/var/www/ombrelloni.it/web'
            error_log: '/var/log/nginx/matteoparrucci.it/error.log'
            access_log: '/var/log/ispconfig/httpd/matteoparrucci.it/access.log'
            media: '/var/www/ombrelloni.it/web/media'
            static: '/var/www/ombrelloni.it/web/static'
