#!/bin/bash

echo step 2

wt=0
#wait /tmp/step 1
while [ $wt -ne 1 ]
do
  wt=$(cat /tmp/step)
  sleep 1
done

sudo hciconfig hcio up
sudo hciconfig hcio
echo 2 > /tmp/step

cd /home/pi
cd BlogCode/btkeyboard/server
while [ 1 ]
do
  sudo python btk_server.py
done

sleep 10
