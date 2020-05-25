#!/bin/bash

echo step 1
sudo /etc/init.d/bluetooth stop
echo 1 > /tmp/step
sudo /usr/sbin/bluetoothd --nodetach --debug -p time

sleep 1
