#!/bin/bash

echo ''
ssh root@192.168.56.107 -t "docker exec root_backend_1 cat /backend_files/pub.pem"
echo ''
