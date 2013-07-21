#!/bin/bash
sshfs vagrant-ombrelloni:/var/www/ombrelloni.it /home/creepingdeath/django/4hm -o uid=$(id -u) -o gid=$(id -g)
cd /home/creepingdeath/django/4hm/django
git config --global user.email "parruc@gmail.com"
git config --global user.name "Matteo Parrucci"
git remote rm origin
git remote add origin git@bitbucket.org:flyingfrog/4hm.git

