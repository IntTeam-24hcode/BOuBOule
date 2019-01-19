#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# test_it.py
#
# Copyright © 2019 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""

"""

from mqttmpd import MQTTMPDController

# instanciating a controller
controller = MQTTMPDController(
    mqtt_broker='mpd.lan',
    mqtt_client_id='mpd_controller',
    mqtt_topicbase='music',
    mqtt_port=1883,
    mpd_server='mpd.lan',
    mpd_port=6600
)

controller.mqtt_connect()

"""
cmd= {
  'command': 'fillColor',
'rgb': [255, 255, 255]
}

controller.launchCMDLaumio(cmd)
/*
cmd= {
  'command': 'animate_raindow'
}
controller.launchCMDLaumio(cmd)
"""
cmd= {
  'command': 'fillColor',
'rgb': [0, 0, 0]
}

controller.launchCMDLaumio(cmd, '4') 

controller.mqtt_client.loop(2)
# loop!
controller.loop_forever()


