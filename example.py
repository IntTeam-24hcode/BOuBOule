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
import json

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

mqttc = controller.mqtt_connect()

cmd= {
  'command': 'fill',
  'rgb': [255, 255, 0]
}
mqttc.publish("laumio/all/json", json.dumps(cmd))
mqttc.loop_forever()
# loop!
controller.loop_forever()


