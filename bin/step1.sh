#!/bin/bash

echo step 1
sudo /etc/init.d/bluetooth stop
sudo /usr/sbin/bluetoothd --nodetach --debug -p time
sleep 1
