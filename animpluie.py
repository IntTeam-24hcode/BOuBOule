import time
import json
import paho.mqtt.client as mqtt

def pluie(client, boule,dt):
    cmds=[]
    cmds1=[]
    rings = [2,1,0]
    for i in rings :
        cmd = {
        'command': 'set_ring',
        'ring': i,
        'rgb': [0, 0, 255]
        }
        cmd1 = {
        'command': 'set_ring',
        'ring': (i+1)%3,
        'rgb': [0, 0, 0]
        }
        cmds.append(cmd)
        cmds1.append(cmd1)
    t=time.time()
    i=0
    while t + dt > time.time():
        client.publish("laumio/{}/json".format(boule), json.dumps(cmds[i]))
        client.publish("laumio/{}/json".format(boule), json.dumps(cmds1[i]))
        i=(i+1)%3
        time.sleep(0.5)

client = mqtt.Client()
client.connect("mpd.lan")
pluie(client, "Laumio_D454DB", 20)




