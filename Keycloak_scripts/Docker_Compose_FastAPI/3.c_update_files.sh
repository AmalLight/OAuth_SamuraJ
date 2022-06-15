#!/bin/bash

chmod 755 -R * && sync

scp -r ./certificates root@192.168.56.107:

scp -r ./postgres_keycloak_data  root@192.168.56.107:
scp -r ./postgres_fastapi_data   root@192.168.56.107:

scp -r ./openldap_data      root@192.168.56.107:
scp -r ./openldap_conf      root@192.168.56.107:
scp -r ./pgadmin_data       root@192.168.56.107:
scp -r ./keycloak_data      root@192.168.56.107:

ssh root@192.168.56.107 -t ' rm -r fastapi_data/*         && sync && chmod 755 -R fastapi_data         '
ssh root@192.168.56.107 -t ' rm -r fastapi_testing_data/* && sync && chmod 755 -R fastapi_testing_data '

scp -r ./fastapi_data          root@192.168.56.107:
scp -r ./fastapi_testing_data  root@192.168.56.107:

ssh root@192.168.56.107 -t ' sync && chmod 755 -R fastapi_data      '
ssh root@192.168.56.107 -t ' docker-compose restart fastapi         '
ssh root@192.168.56.107 -t ' docker-compose restart fastapi_testing '
ssh root@192.168.56.107 -t ' sync && chmod 755 -R certificates      '

scp ./nginx.conf            root@192.168.56.107:
scp ./docker-compose.yml    root@192.168.56.107:
