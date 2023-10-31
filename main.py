import paho.mqtt.client as pahoClient
import time
import uuid


def on_connect(client, userData, flags, responseCode):
    if responseCode == 0:
        print("Connected!")
        return
    print("Bad connection Returned code: {0}", responseCode)


brokerAddress = "172.21.139.119"
mqttConnectionName = str.format("mqtt-pinga-{0}", uuid.uuid4())
mqttClient = pahoClient.Client(mqttConnectionName)
mqttClient.on_connect = on_connect

print("Connecting to the Broker {0}", brokerAddress)

mqttClient.connect(brokerAddress)
mqttClient.loop_start()
mqttClient.publish("/house/main/main-light", "off")
time.sleep(4)
mqttClient.loop_stop()
mqttClient.disconnect()
