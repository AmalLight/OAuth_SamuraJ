#!/bin/bash

ssh root@192.168.56.107 -t ' docker container prune -f ' ;
ssh root@192.168.56.107 -t ' docker image     prune -f ' ;

ssh root@192.168.56.107 -t ' docker rm -f root_postgres_fastapi_1  ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_postgres_keycloak_1 ' ;

ssh root@192.168.56.107 -t ' docker rm -f root_pgadmin_1         ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_fastapi_1         ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_fastapi_testing_1 ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_keycloak_1        ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_nginx_1           ' ;

ssh root@192.168.56.107 -t ' docker rm -f root_phpldapadmin_1 ' ;
ssh root@192.168.56.107 -t ' docker rm -f root_openldap_1     ' ;

ssh root@192.168.56.107 -t ' docker-compose rm -f postgres_fastapi  ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f postgres_keycloak ' ;

ssh root@192.168.56.107 -t ' docker-compose rm -f pgadmin         ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f fastapi         ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f fastapi_testing ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f keycloak        ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f nginx           ' ;

ssh root@192.168.56.107 -t ' docker-compose rm -f openldap     ' ;
ssh root@192.168.56.107 -t ' docker-compose rm -f phpldapadmin ' ;

ssh root@192.168.56.107 -t ' rm -rf /var/lib/docker/volumes/* ' ;

if (( ${#@} >= 1 )) ;
then
     if [[ $1 == 'yes' ]] ; then ssh root@192.168.56.107 -t ' docker image rm root_fastapi         ' ; fi
     if [[ $2 == 'yes' ]] ; then ssh root@192.168.56.107 -t ' docker image rm root_fastapi_testing ' ; fi
fi
