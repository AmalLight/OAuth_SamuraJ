#!/bin/bash

chmod 755 -R * && sync

scp -r ./certificates     root@192.168.56.107:
scp -r ./postgres_data    root@192.168.56.107:
scp -r ./keycloak_data    root@192.168.56.107:

ssh root@192.168.56.107 -t 'rm -r frontend/* && sync && chmod 755 -R frontend' ;

scp -r ./frontend         root@192.168.56.107:

ssh root@192.168.56.107 -t 'sync && chmod 755 -R keycloak_data' ;
ssh root@192.168.56.107 -t 'sync && chmod 755 -R frontend     ' ;
ssh root@192.168.56.107 -t 'sync && chmod 755 -R certificates ' ;

scp ./nginx.conf          root@192.168.56.107:
scp ./docker-compose.yml  root@192.168.56.107:
