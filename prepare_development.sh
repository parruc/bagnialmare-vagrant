#!/bin/bash
GIT_USER=flyingfrog
VAGRANT_DIR=$HOME/Projects/4hm/vm
REPO_DIR=$VAGRANT_DIR/django
echo "repo dir: $REPO_DIR"
sshfs vagrant-ombrelloni:/var/www/ombrelloni.it $VAGRANT_DIR -o uid=$(id -u) -o gid=$(id -g) -o defer_permissions
cd $REPO_DIR
#git config --global user.email "parruc@gmail.com"
#git config --global user.name "Matteo Parrucci"
git remote rm origin
git remote add origin https://$GIT_USER@bitbucket.org/flyingfrog/4hm.git

