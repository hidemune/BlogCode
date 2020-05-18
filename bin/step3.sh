#!/bin/bash
sleep 15

echo step 3
sudo /usr/bin/bluetoothctl <<EOF
agent on
default-agent
scan on
discoverable on
EOF
sleep 10
