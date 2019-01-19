import paho.mqtt.client as mqtt
import time
from random import random, sample
import json

laumios = set()
addVol = 0
updatedVol = True
musicVOL = 50

def toVol(v):
    return max(0, min(100, v))

def on_message(client, userdata, msg):
    global tmin, tmax
    global musicVOL, addVol, updatedVol
    s = str(msg.payload)[2:-1]
    if msg.topic == "laumio/status/advertise":
        if s != "discover" and (s not in laumios):
            laumios.add(s)
    elif msg.topic == "remote/playp/state":
        if s == "ON":
            client.publish("music/control/toggle")
    elif msg.topic == "remote/minus/state" or msg.topic == "remote/plus/state":
        isPlus = msg.topic.count("plus") == 1
        if s == "ON":
            client.publish("music/control/getvol")
            if isPlus:
                tmax = time.time()
            else:
                tmin = time.time()
            updatedVol = False
        else:
            dt = time.time()- (tmax if isPlus else tmin)
            dvol = (1 + max(0, dt - 1) * 3) * (1 if isPlus else -1)
            if updatedVol:
                client.publish("music/control/setvol", toVol(musicVOL + dvol))
            else:
                addVol += dvol
    elif msg.topic == "music/status":
        try:
            musicVOL = int(s[8:])
            if addVol != 0:
                client.publish("music/control/setvol", toVol(musicVOL + addVol))
                addVol = 0
            updatedVol = True
        except:
            pass
    elif msg.topic == "remote/next/state":
        if s == "ON":
            client.publish("music/control/next")
    elif msg.topic == "remote/prev/state":
        if s == "ON":
            client.publish("music/control/previous")
    elif msg.topic == "remote/mute/state":
        if s == "ON":
            client.publish("music/control/setvol", 0)
    else:
        print("Not traited:", msg.topic)
    


client = mqtt.Client()
client.on_message = on_message
client.connect("mpd.lan")
client.subscribe("remote/playp/state")
client.subscribe("remote/minus/state")
client.subscribe("remote/plus/state")
client.subscribe("remote/next/state")
client.subscribe("remote/prev/state")
client.subscribe("remote/mute/state")
client.subscribe("music/status")
client.subscribe("laumio/status/advertise")
client.loop_start()
client.publish("laumio/all/discover")

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