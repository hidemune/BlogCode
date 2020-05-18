#!/bin/bash

sudo apt-get update
sudo apt-get upgrade

sudo apt-get -y install python-gobject bluez bluez-tools bluez-firmware python-bluez python-dev python-pip 
sudo pip install evdev

cd ~/BlogCode/btkeyboard/dbus
sudo cp org.yaptb.btkkbservice.conf /etc/dbus-1/system.d

