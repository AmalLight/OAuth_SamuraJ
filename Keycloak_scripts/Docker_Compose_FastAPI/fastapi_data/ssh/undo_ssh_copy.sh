#!/bin/bash

echo 'authorized keys'
sshpass -p REPLACE1 ssh REPLACE2 -t 'cat   /root/.ssh/authorized_keys'

echo 'old authorized keys 2'
sshpass -p REPLACE1 ssh REPLACE2 -t 'cat   /root/.ssh/authorized_keys_2'

sshpass -p REPLACE1 ssh REPLACE2 -t 'rm -f /root/.ssh/authorized_keys_2'

echo 'new authorized keys 2'
sshpass -p REPLACE1 ssh REPLACE2 -t '[[ -f /root/.ssh/authorized_keys_2 ]] && cat /root/.ssh/authorized_keys_2'
