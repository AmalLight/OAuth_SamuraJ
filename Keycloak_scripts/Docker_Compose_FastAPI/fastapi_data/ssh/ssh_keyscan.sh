#!/bin/bash

scan=`  ssh-keyscan -H REPLACE 2> /dev/null `
known=` cat /root/.ssh/known_hosts          `

[[ "$known" != *"$scan"* ]] && printf "%s\n" "$scan" >> /root/.ssh/known_hosts
