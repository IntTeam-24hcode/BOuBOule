import paho.mqtt.client as mqtt
import time
from random import random, sample
import json

laumios = set()
musicON = False
def next_song(client):
    client.publish("music/control/next")

def prev_song(client):
    client.publish("music/control/previous")

def mute_song(client):
    client.publish("music/control/setvol", 0)


def on_message(client, userdata, msg):
    global musicON
    s = str(msg.payload)[2:-1]
    if msg.topic == "laumio/status/advertise":
        if s != "discover" and (s not in laumios):
            laumios.add(s)
    elif msg.topic == "remote/playp/state":
        if s == "ON":
            client.publish("music/control/{}".format("pause" if musicON else "play"))
            musicON = not musicON
    elif msg.topic == "music/status":
        if s.startswith("state:"):
            musicON = s == "state: play"
    elif msg.topic == "remote/next/state":
        next_song(client)
    elif msg.topic == "remote/prev/state":
        prev_song(client)
    else:
        print("Not traited:", msg.topic)

client = mqtt.Client()
client.on_message = on_message
client.connect("mpd.lan")
client.subscribe("remote/playp/state")
client.subscribe("laumio/status/advertise")
client.subscribe("music/status")
client.publish("music/control/getstate")
client.loop_start()
client.publish("laumio/all/discover")
