import json
from time import sleep
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

# def on_mes(self, )

mqttc = controller.mqtt_connect()
mqttc.subscribe("laumio/status/advertise")
mqttc.publish("laumio/all/discover")
mqttc.subscribe("capteur_bp/status")
mqttc.subscribe("capteur_bp/switch/1/state")
mqttc.subscribe("capteur_bp/binary_sensor/1/state")

cmd= {
  'command': 'fill',
  'rgb': [255, 0, 0]
}
cmd2 = {
  'command': 'animate_rainbow'
}
cmd3 = {
  'command': 'fill',
  'rgb': [0, 0, 255]
}

# mqttc.publish("laumio/Laumio_10805F/json", json.dumps(cmd))
# sleep(1)
# mqttc.publish("laumio/Laumio_107DA8/json", json.dumps(cmd3))
# sleep(1)
# mqttc.publish("laumio/Laumio_104F03/json", json.dumps(cmd))
#coucou 
mqttc.loop_forever()
#mqttc.publish("laumio/all/json", json.dumps(cmd2))

controller.loop_forever()