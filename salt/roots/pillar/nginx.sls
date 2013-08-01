nginx:
    hosts:
        ombrelloni:
            {% if grains['configuration'] == 'local' %}
            server_name : 'ombrelloni.it'
            {% elif grains['configuration'] == 'dev' %}
            server_name : 'dev.creepingserver.it'
            {% else %}
            server_name : 'da decidere'
            {% endif %}
            root: '/var/www/ombrelloni.it'
            web: '/var/www/ombrelloni.it/web'
            error_log: '/var/www/ombrelloni.it/log/error.log'
            access_log: '/var/www/ombrelloni.it/log/access.log'
            error_pages: '/var/www/ombrelloni.it/web/error'
            analitycs_id: ''
            media: '/var/www/ombrelloni.it/web/media'
            static: '/var/www/ombrelloni.it/web/static'
            doc: '/var/www/ombrelloni.it/web/doc'
