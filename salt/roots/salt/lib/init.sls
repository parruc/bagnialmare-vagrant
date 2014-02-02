lib_repo_prereq:
    pkg.installed:
        - name: python-apt

lib_repo_remove:
    pkgrepo.absent:
        - names:
            - deb http://ftp.it.debian.org/debian/ wheezy main
            - deb-src http://ftp.it.debian.org/debian/ wheezy main
            - deb http://ftp.it.debian.org/debian/ wheezy-updates main
            - deb-src http://ftp.it.debian.org/debian/ wheezy-updates main
        - require:
            - pkg: lib_repo_prereq

lib_repo_add:
    pkgrepo.managed:
        - names:
            - deb http://mi.mirror.garr.it/mirrors/debian wheezy main
            - deb-src http://mi.mirror.garr.it/mirrors/debian wheezy main
            - deb http://mi.mirror.garr.it/mirrors/debian wheezy-updates main
            - deb-src http://mi.mirror.garr.it/mirrors/debian wheezy-updates main
            - deb http://security.debian.org wheezy/updates main
            - deb-src http://security.debian.org wheezy/updates main
            - deb http://debian.saltstack.com/debian wheezy-saltstack main
        - require:
            - pkg: lib_repo_prereq


lib_reqs:
    pkg.installed:
        - names:
            - gettext
            - libgdal-dev
            - libjpeg8
            - libjpeg8-dev
            - libxml2
            - libxml2-dev
            - libxslt1.1
            - libxslt1-dev
            - libtiff4
            - libtiff4-dev
            - libzip2
            - libzip-dev
        - require:
            - pkgrepo: lib_repo_remove
            - pkgrepo: lib_repo_add
