#!/bin/bash

ssh root@192.168.56.107 -t sh -c 'apt update ; \
    \
    apt upgrade -y ; \
    \
    apt install -y docker docker-compose docker.io ; '
