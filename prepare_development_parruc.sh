#!/bin/bash

#change this to your username in bitbucket
GIT_USER=parruc

#change this to project directory on your machine
HOST_DIR=$HOME/projects/django/bagnialmare

GUEST_DIR=vagrant-ombrelloni:/var/www/ombrelloni.it

CWD=$(pwd)

echo "mounting $GUEST_DIR to $HOST_DIR"
sudo mount -t cifs //192.168.50.2/ombrelloni $HOST_DIR -o username=ombrelloni,password=ombrelloni,uid=creepingdeath
echo "changing git credentials for your user: $GIT_USER"
cd "$HOST_DIR/django"
if [ "$PWD"=="$HOST_DIR/django" ]; then
    git config --global user.email "parruc@gmail.com"
    git config --global user.name "Matteo Parrucci"
    git config master.autosetuprebase always
#    git remote rm origin
#    git remote add origin https://$GIT_USER@bitbucket.org/flyingfrog/4hm.git
fi


#cd $CWD
#launch selenium local server
#java -jar selenium
#forward guest selenium port to host
#vagrant ssh -- -f -R 4444:localhost:4444 -N
