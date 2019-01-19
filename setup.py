import paho.mqtt.client as mqtt
import time
from random import random, sample
import json


def on_message(client, userdata, msg):
    pass

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost")
client.publish("hello/world", "world")
client.loop_start()