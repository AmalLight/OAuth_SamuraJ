#!/bin/bash

authorized='AuthorizedKeysFile .ssh/authorized_keys .ssh/authorized_keys_2'

config=` sshpass -p REPLACE1 ssh REPLACE2 -t "cat /etc/ssh/sshd_config | grep '$authorized'" `
echo "old sshd_config: $config"

if [[ "$config" != *"$authorized"* ]];
then
     sshpass -p REPLACE1 ssh REPLACE2 -t "echo '$authorized' >> /etc/ssh/sshd_config"
     
     echo "new sshd_config: $config"
     sshpass -p REPLACE1 ssh REPLACE2 -t "cat /etc/ssh/sshd_config | grep '$authorized'"
     
     sshpass -p REPLACE1 ssh REPLACE2 -t 'systemctl restart sshd'
fi

echo 'authorized keys'
sshpass -p REPLACE1 ssh REPLACE2 -t 'cat .ssh/authorized_keys'

sshpass -p REPLACE1 scp /root/.ssh/authorized_keys_2 REPLACE2:/root/.ssh/authorized_keys_2

echo 'authorized keys 2'
sshpass -p REPLACE1 ssh REPLACE2 -t 'cat .ssh/authorized_keys_2'
