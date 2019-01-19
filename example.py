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

cmd= {
  'command': 'fill',
  'rgb': [0, 255, 0]
}
cmd2 = {
  'command': 'animate_rainbow'
}
cmd3 = {
  'command': 'set_column',
  'column': 0,
  'rgb': [200, 56, 200]
}
mqttc.publish("laumio/Laumio_1D9486/json", json.dumps(cmd))
# sleep(2)
#mqttc.publish("laumio/all/json", json.dumps(cmd2))
mqttc.loop_forever()

controller.loop_forever()