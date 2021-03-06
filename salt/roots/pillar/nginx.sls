{% set dev = grains['configuration'] in ['local', 'dev'] %}
nginx:
    hosts:
        ombrelloni:
            {% if grains['configuration'] == 'local' %}
            server_name : 'loc.bagnialmare.com'
            {% elif grains['configuration'] == 'dev' %}
            server_name : 'dev.bagnialmare.com'
            {% elif  grains['configuration'] == 'prod' %}
            server_name : 'bagnialmare.com'
            {% endif %}
            root: '/var/www/ombrelloni.it'
            web: '/var/www/ombrelloni.it/web'
            error_log: '/var/www/ombrelloni.it/log/error.log'
            access_log: '/var/www/ombrelloni.it/log/access.log'
            error_pages: '/var/www/ombrelloni.it/web/error'
            analitycs_id: ''
            media: '/var/www/ombrelloni.it/web/media'
            static: '/var/www/ombrelloni.it/web/static'
            {% if dev %}
            coverage: '/var/www/ombrelloni.it/web/coverage'
            doc: '/var/www/ombrelloni.it/web/doc'
            {% endif %}
