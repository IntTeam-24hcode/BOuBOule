import paho.mqtt.client as mqtt
import time
from random import random, sample
import json

laumios = set()
musicON = False

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
# client.publish("music/control/pause")

time.sleep(1)
for _ in range(500):
    time.sleep(0.1)
    cmd = {
        'command': 'fill',
        'rgb': [int(random()*256), int(random()*256), int(random()*256)]
    }
    # client.publish("laumio/{}/json".format(sample(laumios, 1)[0]), json.dumps(cmd))
# client.subscribe("capteur_bp/binary_sensor/bp1/state")
# client.publish("music/control/play")
# time.sleep(1)
# client.publish("music/control/pause")
# time.sleep(1)
# client.publish("music/control/play")