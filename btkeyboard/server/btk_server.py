#!/usr/bin/python
#
# YAPTB Bluetooth keyboard emulator DBUS Service
# 
# Adapted from 
# www.linuxuser.co.uk/tutorials/emulate-bluetooth-keyboard-with-the-raspberry-pi
#
#

#from __future__ import absolute_import, print_function, unicode_literals
from __future__ import absolute_import, print_function

from optparse import OptionParser, make_option
import os
import sys
import uuid
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import bluetooth
from bluetooth import *
import subprocess
from time import sleep 

import gtk
from dbus.mainloop.glib import DBusGMainLoop

global gBDADDR
#gBDADDR = "CC:82:EB:97:46:DC"

#
#define a bluez 5 profile object for our keyboard
#
class BTKbBluezProfile(dbus.service.Object):
    fd = -1
    

    @dbus.service.method("org.bluez.Profile1",
                                    in_signature="", out_signature="")
    def Release(self):
            print("Release")
            mainloop.quit()

    @dbus.service.method("org.bluez.Profile1",
                                    in_signature="", out_signature="")
    def Cancel(self):
            print("Cancel")

    @dbus.service.method("org.bluez.Profile1", in_signature="oha{sv}", out_signature="")
    def NewConnection(self, path, fd, properties):
            self.fd = fd.take()
            print("NewConnection(%s, %d)" % (path, self.fd))
            for key in properties.keys():
                    if key == "Version" or key == "Features":
                            print("  %s = 0x%04x" % (key, properties[key]))
                    else:
                            print("  %s = %s" % (key, properties[key]))
            


    @dbus.service.method("org.bluez.Profile1", in_signature="o", out_signature="")
    def RequestDisconnection(self, path):
            print("RequestDisconnection(%s)" % (path))

            if (self.fd > 0):
                    os.close(self.fd)
                    self.fd = -1

    def __init__(self, bus, path):
            dbus.service.Object.__init__(self, bus, path)


#
#create a bluetooth device to emulate a HID keyboard, 
# advertize a SDP record using our bluez profile class
#
class BTKbDevice():
    #change these constants sudo hciconfig hcio
    ret = subprocess.check_output("hciconfig hcio | grep Address", shell=True)
    args = ret.decode("utf-8").split(" ")
    print(args[3])
    MY_ADDRESS=args[3]
    MY_DEV_NAME="RasPi_BTKb"

    #define some constants
    P_CTRL =17  #Service port - must match port configured in SDP record
    P_INTR =19  #Service port - must match port configured in SDP record#Interrrupt port  
    PROFILE_DBUS_PATH="/bluez/yaptb/btkb_profile" #dbus path of  the bluez profile we will create
    SDP_RECORD_PATH = sys.path[0] + "/sdp_record.xml" #file path of the sdp record to laod
    UUID="00001124-0000-1000-8000-00805f9b34fb"
             
 
    def __init__(self):

        print("Setting up BT device")

        self.init_bt_device()
        self.init_bluez_profile()
                    

    #configure the bluetooth hardware device
    def init_bt_device(self):


        print("Configuring for name "+BTKbDevice.MY_DEV_NAME)

        #set the device class to a keybord and set the name
        os.system("hciconfig hcio class 0x002540")
        os.system("hciconfig hcio name " + BTKbDevice.MY_DEV_NAME)

        #make the device discoverable
        os.system("hciconfig hcio piscan")


    #set up a bluez profile to advertise device capabilities from a loaded service record
    def init_bluez_profile(self):

        print("Configuring Bluez Profile")

        #setup profile options
        service_record=self.read_sdp_service_record()

        opts = {
            "ServiceRecord":service_record,
            "Role":"server",
            "RequireAuthentication":False,
            "RequireAuthorization":False
        }

        #retrieve a proxy for the bluez profile interface
        bus = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("org.bluez","/org/bluez"), "org.bluez.ProfileManager1")

        profile = BTKbBluezProfile(bus, BTKbDevice.PROFILE_DBUS_PATH)

        manager.RegisterProfile(BTKbDevice.PROFILE_DBUS_PATH, BTKbDevice.UUID,opts)

        print("Profile registered ")


    #read and return an sdp record from a file
    def read_sdp_service_record(self):

        print("Reading service record")

        try:
            fh = open(BTKbDevice.SDP_RECORD_PATH, "r")
        except:
            sys.exit("Could not open the sdp record. Exiting...")

        return fh.read()   



    #listen for incoming client connections
    #ideally this would be handled by the Bluez 5 profile 
    #but that didn't seem to work
    def listen(self):

        print("Waiting for connections")
        self.scontrol=BluetoothSocket(L2CAP)
        self.sinterrupt=BluetoothSocket(L2CAP)

        #bind these sockets to a port - port zero to select next available		
        self.scontrol.bind((self.MY_ADDRESS,self.P_CTRL))
        self.sinterrupt.bind((self.MY_ADDRESS,self.P_INTR ))

        #Start listening on the server sockets 
        self.scontrol.listen(1) # Limit of 1 connection
        self.sinterrupt.listen(1)

        self.ccontrol,cinfo = self.scontrol.accept()
        print ("Got a connection on the control channel from " + cinfo[0])

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print ("Got a connection on the interrupt channel from " + cinfo[0])
        gBDADDR = cinfo[0]
        os.system ("echo " + gBDADDR + "> /tmp/gBDADDR")

    #send a string to the bluetooth host machine
    def send_string(self,message):
      try:
         #print("Sending "+message)
         self.cinterrupt.send(message)
      except:
        #print ("Connect2gBDADDR:" + gBDADDR)
        if True :
         # Hidemune!!!
         #self.listen();
         
         self.ccontrol.close();
         self.cinterrupt.close();
         self.ccontrol=BluetoothSocket(L2CAP)
         self.cinterrupt=BluetoothSocket(L2CAP)
         #self.ccontrol.bind(( self.MY_ADDRESS, self.P_CTRL ))
         #self.cinterrupt.bind(( self.MY_ADDRESS, self.P_INTR ))
         ret = subprocess.check_output("cat /tmp/gBDADDR", shell=True)
         gBDADDR = ret.decode("utf-8").strip()
         print (gBDADDR)
         self.ccontrol.connect(( gBDADDR, self.P_CTRL ));
         self.cinterrupt.connect(( gBDADDR, self.P_INTR ));
         sleep(0.050);
         pass
        else:
         self.listen();

#define a dbus service that emulates a bluetooth keyboard
#this will enable different clients to connect to and use 
#the service
class  BTKbService(dbus.service.Object):

    def __init__(self):

        print("Setting up service")

        #set up as a dbus service
        bus_name=dbus.service.BusName("org.yaptb.btkbservice",bus=dbus.SystemBus())
        dbus.service.Object.__init__(self,bus_name,"/org/yaptb/btkbservice")

        #create and setup our device
        self.device= BTKbDevice();

        #start listening for connections
        if False: #gBDADDR != "":
          self.scontrol = BluetoothSocket(L2CAP)
          self.sinterrupt = BluetoothSocket(L2CAP)
          self.scontrol.connect((gBDADDR, self.device.P_CTRL))
          self.sinterrupt.connect((gBDADDR, self.device.P_INTR))
        else:
          self.device.listen();

            
    @dbus.service.method('org.yaptb.btkbservice', in_signature='yay')
    def send_keys(self,modifier_byte,keys):

        cmd_str=""
        cmd_str+=chr(0xA1)
        cmd_str+=chr(0x01)
        cmd_str+=chr(modifier_byte)
        cmd_str+=chr(0x00)

        count=0
        for key_code in keys:
            if(count<6):
                cmd_str+=chr(key_code)
            count+=1

        self.device.send_string(cmd_str);		


#main routine
if __name__ == "__main__":
    # we an only run as root
    if not os.geteuid() == 0:
       sys.exit("Only root can run this script")
    gBDADDR = ""

    DBusGMainLoop(set_as_default=True)
    myservice = BTKbService();
    gtk.main()
    
