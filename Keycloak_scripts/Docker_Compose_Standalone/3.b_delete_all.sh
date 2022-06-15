#!/bin/bash

ssh root@192.168.56.107 -t 'yes | docker container prune' ;

ssh root@192.168.56.107 -t 'docker rm -f root_postgres_1' ;
ssh root@192.168.56.107 -t 'docker rm -f root_frontend_1' ;
ssh root@192.168.56.107 -t 'docker rm -f root_keycloak_1' ;
ssh root@192.168.56.107 -t 'docker rm -f root_nginx_1   ' ;

ssh root@192.168.56.107 -t 'docker-compose rm -f postgres' ;
ssh root@192.168.56.107 -t 'docker-compose rm -f frontend' ;
ssh root@192.168.56.107 -t 'docker-compose rm -f keycloak' ;
ssh root@192.168.56.107 -t 'docker-compose rm -f nginx   ' ;

ssh root@192.168.56.107 -t 'yes | docker image prune ' ;

ssh root@192.168.56.107 -t 'rm -rf /var/lib/docker/volumes/*' ;

if (( ${#@} >= 1 )) ;
then
     if [[ $1 == 'yes' ]] ;
     then
         ssh root@192.168.56.107 -t 'docker image rm root_frontend' ;
     fi
fi

ssh root@192.168.56.107 -t 'docker network rm root_keycloak-network-backend' ;
