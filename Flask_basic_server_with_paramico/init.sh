#!/bin/bash

pip3 install --upgrade pip

pip3 install flask-appbuilder authlib
pip3 install paramiko pillow

bash ./connect.sh

# flask fab create-app && flask run
