#!/bin/bash

rm ./certificates/* && sync

openssl genrsa -out ./certificates/host.key 2048

openssl req -new -x509 -nodes -sha256 -days 365 -key ./certificates/host.key \
                                                -out ./certificates/host.crt
chmod  755 -R ./certificates/
echo '' && ls ./certificates/ && echo ''
