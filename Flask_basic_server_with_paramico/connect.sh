chmod 775 *
echo *** | sudo -S cp *.service /etc/systemd/system/

els=`ls *.service`

sudo systemctl daemon-reload

for el in $els;
do
    sudo systemctl stop    $el
    sudo systemctl start   $el
    sudo systemctl enable  $el
    sudo systemctl restart $el
done

sudo systemctl daemon-reload
