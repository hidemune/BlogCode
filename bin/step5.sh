#!/bin/bash

# (Remember to have the bluetooth deamon running in a 
# separate terminal window before doing this)
echo step 5
cd
cd BlogCode/btkeyboard/keyboard
while [ 1 ]
do
  sudo python kb_client.py
done
sleep 10
