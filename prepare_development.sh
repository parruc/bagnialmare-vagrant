#!/bin/bash

#change this to your username in bitbucket
GIT_USER=flyingfrog

#change this to project directory on your machine
HOST_DIR=$HOME/Projects/4hm/vm

GUEST_DIR=vagrant-ombrelloni:/var/www/ombrelloni.it

echo "mounting $GUST_DIR to $HOST_DIR"
sshfs $GUEST_DIR $HOST_DIR -o uid=$(id -u) -o gid=$(id -g) -o defer_permissions
echo "changing git credentials for your user: $GIT_USER"
cd $HOST_DIR/django
#git config --global user.email "parruc@gmail.com"
#git config --global user.name "Matteo Parrucci"
git remote rm origin
git remote add origin https://$GIT_USER@bitbucket.org/flyingfrog/4hm.git

#launch selenium local server
java -jar selenium
#forward guest selenium port to host
vagrant ssh -- -f -R 4444:localhost:4444 -N
