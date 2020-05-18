#!/bin/bash

echo step 2
sudo hciconfig hcio up
sudo hciconfig hcio

cd /home/pi
cd BlogCode/btkeyboard/server
while [ 1 ]
do
  sudo python btk_server.py
done

sleep 10
