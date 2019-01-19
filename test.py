import paho.mqtt.client as mqtt
import l

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.connect("mpd.lan", 1883, 60)

cmd = "{ 'command': 'fill', 'rgb': [255, 0, 0] }"

client.loop_forever()