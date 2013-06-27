python-pip:
    pkg.installed

virtualenvwrapper:
    pip.installed

/var/virtualenv:
    virtualenv.managed:
        - no_site_packages: True
