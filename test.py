import paho.mqtt.client as mqtt
import time
from random import random, sample
import json

laumios = set()
addVol = 0

def on_message(client, userdata, msg):
    global tmin, tmax
    global musicVOL
    s = str(msg.payload)[2:-1]
    if msg.topic == "laumio/status/advertise":
        if s != "discover" and (s not in laumios):
            laumios.add(s)
    elif msg.topic == "remote/playp/state":
        if s == "ON":
            client.publish("music/control/toggle")
    elif msg.topic == "remote/minus/state":
        if s == "ON":
            client.publish("music/control/getvol")
            tmin=time.time()
        else:
            dt= time.time()-tmin
    elif msg.topic == "music/status":
        try:
            musicVOL = int(s)
        except:
            pass
    


        


    else:
        print("Not traited:", msg.topic)
    


client = mqtt.Client()
client.on_message = on_message
client.connect("mpd.lan")
client.subscribe("remote/playp/state")
client.subscribe("remote/minus/state")
client.subscribe("laumio/status/advertise")
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