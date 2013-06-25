import sys, os
from fabric.api import run, env, sudo, hide, settings, cd, require
from fabric.contrib import django, files

env.project_name = 'ombrelloni'

sys.path.insert(0, os.path.abspath('.'))

django.project(env.project_name)
django.settings_module('%(project_name)s.settings' % env)
from django.conf import settings as django_settings
db_settings = django_settings.DATABASES

### Define Deploy target ###
def dev():
    "Use dev server as deploy target"
    env.hosts = ["creepingdeath@creepingserver.it:2200"]
    env.path = '/opt/django/%(project_name)s' % env
    env.db = "dev"

def local():
    "Use the local virtual server as deploy target [default]"
    env.hosts = ['localhost']
    env.path = os.path.abspath('.')
    env.db = "local"

local()

### Define platform ###

def debian():
    "Use debian like OS [default]"
    env.installation_command = "apt-get install --quiet --assume-yes"
    env.installation_packages = "libjpeg libjpeg-dev libxml2 libxml2-dev lixslt libxslt-dev libtiff libtiff-dev libzip postgresql-9.1 postgresql-server-dev-9.1 postgresql-9.1-postgis"
    env.db_config_path = "/etc/postgresql/9.1/main/pg_hba.conf"
debian()

def opensuse():
    "Use opensuse OS"
    env.installation_command = "zypper install --auto-agree-with-licenses"
    env.installation_packages = "libjpeg62 libjpeg62-devel libxml2 libxml2-devel lixslt1 libxslt-devel libtiff5 libtiff-devel libzip2 postgresql91 postgresql91-devel postgresql91-server postgis2 python python-pip"
    env.db_config_path = "/var/lib/pgsql/data/pg_hba.conf"

### Installation stuff ###

def fix_db_settings():
    """Fixes authentication method in setup file
    """
    files.sed(env.db_config_path, "^(host.+?)peer", "\1md5", use_sudo=True)

def system_requirements():
    """Installs system requirements
    """
    require('installation_command')
    require('installation_packages')
    sudo("%(installation_command)s %(installation_packages)s" % env)
    fix_db_settings()
    restart_db()

def virtualenv_exists():
    return env.project_name in run('lsvirtualenv', capture=True).split()

def setup_virtualenv():
    run("pip install virtualenv virtualenvwrapper")
    if not virtualenv_exists():
        run("mkvirtualenv %(project_name)s --no-site-packages" % env)
    run("workon %(project_name)s" % env)
    run("pip install -r requirements.txt")
    with cd(env.path):
        run("chmod a+x manage.py")
        run("./manage.py syncdb")
        run("./manage.py migrate")

### DATA IMPORT ###

def import_data():
    """Imports data from scraped sources
    """
    with cd('%(path)s/scripts/scraping' % env):
        run("python import_cervia.py")
        run("python import_cesenatico.py")
        run("python import_ravenna.py")
    with cd(env.path):
        run("./manage.py import_services")
        run("./manage.py import_bagni")

### DB RELATED STUFF ###

def _run_as_pg(command):
    """
    Run command as 'postgres' user
    """
    return sudo('sudo -u postgres %s' % command)

def user_exists(name):
    """
    Check if a PostgreSQL user exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(name)s';"''' % locals())
    return (res == "1")

def database_exists(name):
    """
    Check if a PostgreSQL database exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        return _run_as_pg('''psql -d %(name)s -c ""''' % locals()).succeeded

def restart_db():
    """Restarts postgresql process
    """
    sudo("/etc/init.d/postgresql restart")

def create_db():
    """Creates DB and installs GIS extension
    """
    if not database_exists('ombrelloni'):
        db = "psql -c 'CREATE DATABASE %(NAME)s;'"
        _run_as_pg(db % db_settings[env.db])
    _run_as_pg("psql -c 'CREATE EXTENSION IF NOT EXISTS postgis;'")

def drop_db():
    """Deletes DB
    """
    if database_exists('ombrelloni'):
        db = "psql -c 'DROP DATABASE %(NAME)s;'"
        _run_as_pg(db % db_settings[env.db])

def create_db_user():
    """Creates the DB user
    """
    if not user_exists(db_settings[env.db]['USER']):
        command = "psql -c 'CREATE USER %(USER)s WITH PASSWORD %(PASSWORD)s;'"
        _run_as_pg(command % db_settings[env.db])

def grant_db_privileges():
    """Grants our user rights for the db
    """
    if database_exists(db_settings[env.db]['NAME']) and \
        user_exists(db_settings[env.db]['USER']):
        grant = "psql -c 'GRANT ALL PRIVILEGES ON DATABASE %(NAME)s to %(USER)s';"
        _run_as_pg(grant % db_settings[env.db])

def dump_db():
    """Dumps the DB into dump.sql file
    """
    if database_exists(db_settings[env.db]['NAME']):
        with cd(env.path):
            _run_as_pg("pg_dump %(NAME)s > dump.sql" % db_settings[env.db])

def restore_db():
    """Restores the DB from dump.sql file
    """
    if not database_exists(db_settings[env.db]['NAME']):
        create_db()
    with cd(env.path):
        _run_as_pg("psql %(NAME)s < dump.sql" % db_settings[env.db])

def setup_db():
    """Create db user, creates db, and grants privileges
    """
    create_db_user()
    create_db()
    grant_db_privileges()

def recreate_db():
    """Deletes and recreates DB
    """
    drop_db()
    setup_db()
