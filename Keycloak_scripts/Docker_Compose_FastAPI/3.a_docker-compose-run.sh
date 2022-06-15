#!/bin/bash

ssh root@192.168.56.107 -t 'iptables -t filter -F ; iptables -t nat -F ; iptables -t mangle -F'

sleep 1 && ssh root@192.168.56.107 -t 'service docker stop '
sleep 1 && ssh root@192.168.56.107 -t 'service docker start'

echo ''

sleep 1 && ssh root@192.168.56.107 -t 'apt update'

echo ''

ssh root@192.168.56.107 -t 'service docker restart' && sleep 1

bash 3.b_delete_all.sh "$@"

bash 3.c_update_files.sh

ssh root@192.168.56.107 -t 'chmod 777 -R /root/ ; chmod 755 /root/ ; chmod 755 -R /root/.ssh/ '

ssh root@192.168.56.107 -t 'ln -sf /usr/share/zoneinfo/Europe/Rome /etc/localtime && echo "" && date && echo ""'

ssh root@192.168.56.107 -t 'docker-compose up'
