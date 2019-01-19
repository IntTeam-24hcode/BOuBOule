import time
import json
import paho.mqtt.client as mqtt

def spiral(client, boule, temps):
	cmds = []
	resets = []
	order = [10, 2, 7, 4, 12, 0, 6, 5, 11, 1, 3, 8, 9]
	for i in order:
		center = i / 12 * 3 * 256
		R = max([0, 255 - center, center - 2*256])
		G = abs(255 - center) if center < 2*256-1 else 0
		B = abs(2*256 - center) if center > 256 else 0
		cmd = {
		  'command': 'set_pixel',
		  'led': i,
		  'rgb': [R, G, B]
		}
		cmds.append(cmd)
		reset = {
			'command': 'set_pixel',
			'led': i,
			'rgb': [0, 0, 0]
		}
		resets.append(reset)
	t = time.time()
	i = 0
	print("coucou", t, temps, time.time())
	while t + temps > time.time():
		print("test")
		client.publish("laumio/{}/json".format(boule), json.dumps(resets[i]))
		i = (i+1) % 13
		client.publish("laumio/{}/json".format(boule), json.dumps(cmds[i]))
		time.sleep(0.1)

client = mqtt.Client()
client.connect("mpd.lan")
spiral(client, "Laumio_D454DB", 20)