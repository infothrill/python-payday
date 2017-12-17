#!/bin/bash

sudo apt-get update
sudo apt-get install -y python-setuptools python-pip python-virtualenv python-dev wkhtmltopdf xvfb

virtualenv $HOME/env
source $HOME/env/bin/activate
cd /vagrant/ && python setup.py develop
