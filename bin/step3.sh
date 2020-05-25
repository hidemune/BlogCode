#!/bin/bash

echo step 3

wt=0
#wait /tmp/step 2
while [ $wt -ne 2 ]
do
  wt=$(cat /tmp/step)
  sleep 1
done

sudo /usr/bin/bluetoothctl <<EOF
agent on
default-agent
scan on
discoverable on
EOF
sleep 10
