import paho.mqtt.client as mqtt
import time
from random import random, sample
import json

laumios = set()
selec = -1
selected = set()
isPlaying = False
answer = None

def on_message(client, userdata, msg):
	global selec, answer, isPlaying, lampes, selected
	s = str(msg.payload)[2:-1]
	if msg.topic == "laumio/status/advertise":
		if s != "discover" and (s not in laumios):
			laumios.add(s)
	elif isPlaying and msg.topic.startswith("remote/") and msg.topic.endswith("/state"):
		if s == "ON":
			i = int(msg.topic[7])
			if selec == i:
				answer = i
			elif i not in selected:
				if selec != -1:
					client.publish("laumio/{}/json".format(lampes[selec]), json.dumps(comBlack))
				selec = i
				client.publish("laumio/{}/json".format(lampes[i]), json.dumps(comBlue))

client = mqtt.Client()
client.on_message = on_message
client.connect("mpd.lan")
for i in range(10):
	client.subscribe("remote/{}/state".format(i))
client.subscribe("laumio/status/advertise")
client.loop_start()
client.publish("laumio/all/discover")

time.sleep(1.5)
comBlue = { 'command': 'fill', 'rgb': [0, 0, 255] }
comBlack = { 'command': 'fill', 'rgb': [0, 0, 0] }
comGreen = { 'command': 'fill', 'rgb': [0, 255, 0] }
comRed = { 'command': 'fill', 'rgb': [255, 0, 0] }
client.publish("laumio/all/json", json.dumps(comBlack))

# lampes = sample(laumios, 10)
lampes = ["Laumio_1D9486", "Laumio_104A13", "Laumio_0FBFBF",
		  "Laumio_104F03", "Laumio_10508F", "Laumio_10805F",
		  "Laumio_CD0522", "Laumio_0FC168", "Laumio_D454DB", "Laumio_107DA8"]
t = 1.5
n = 2
while True:
	ls = sample(list(range(10)), n)
	for l in ls:
		client.publish("laumio/{}/json".format(lampes[l]), json.dumps(comBlue))
	time.sleep(t)
	for l in ls:
		client.publish("laumio/{}/json".format(lampes[l]), json.dumps(comBlack))
	m = 0
	selected = set()
	isPlaying = True
	while m < n:
		selec = -1
		answer = None
		while answer == None:
			time.sleep(0.1)
		if answer in ls:
			selec = -1
			selected.add(answer)
			client.publish("laumio/{}/json".format(lampes[answer]), json.dumps(comGreen))
			m += 1
		else:
			client.publish("laumio/{}/json".format(lampes[answer]), json.dumps(comRed))
			break
	isPlaying = False
	time.sleep(0.5)
	if m == n:
		client.publish("laumio/all/json", json.dumps(comGreen))
		t *= 0.9
		if t < 0.6:
			n = 5
		elif t < 0.9:
			n = 4
		elif t < 1.2:
			n = 3
	else:
		client.publish("laumio/all/json", json.dumps(comRed))
	time.sleep(1)
	client.publish("laumio/all/json", json.dumps(comBlack))