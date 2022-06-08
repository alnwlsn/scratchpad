#simple mqtt to x10 bridge - alnwlsn 2022
#starting from example at https://www.eclipse.org/paho/index.php?page=clients/python/index.php
#which is probably an example from the paho docs

#converts mqtt messages to X10 commands using heyu

#to turn on device C5, send "on" to x10/c5 - that's it

import paho.mqtt.client as mqtt
import re
import os

def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    client.subscribe("x10/#")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf8').lower()
    tsplit = msg.topic.lower().split('/')
    # print(tsplit,payload)
    if(bool(re.search("[a-p]\d",tsplit[1]))): #if looks like an x10 address
        if(payload in ["on","off"]): #allowed payloads
            cmd = "heyu "+payload+" "+tsplit[1]
            os.system(cmd)
            # print(cmd)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.31", 1883, 60)

client.loop_forever()