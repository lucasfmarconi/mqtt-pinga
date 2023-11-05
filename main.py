import sys
import time
import paho.mqtt.client as pahoClient
import uuid


def on_log(client, userdata, level, buf):
    print("log:", buf)


def on_connect_fail(client, userData):
    print("Connection failed")


def on_connect(client, userData, flags, responseCode):
    match responseCode:
        case 0:
            print("MQTT Client connected")
            return
        case 1:
            print(
                "The server does not support the MQTT protocol requested by the client"
            )
        case 2:
            print(
                "The client ID is the correct UTF-8 string, but is not allowed by the server"
            )
        case 3:
            print(
                "Network connection has been established, but MQTT service is unavailable"
            )
        case 4:
            print("The data in the username or password is in the wrong format")
        case 5:
            print("Client connection is not authorized")

    if responseCode != 0:
        client.loop_stop()


brokerAddress = "localhost"
mqttConnectionName = str.format("pinga-client-{0}", uuid.uuid4())
mqttClient = pahoClient.Client(mqttConnectionName)
mqttClient.on_connect = on_connect
mqttClient.on_connect_fail = on_connect_fail
mqttClient.on_log = on_log
# mqttClient.tls_set()
# mqttClient.tls_insecure_set(True)
# mqttClient.username_pw_set("", "")

print("Connecting to the Broker", brokerAddress)
try:
    mqttClient.connect(brokerAddress, port=1883)
except:
    print("Unable to connect to the broker", brokerAddress)
    sys.exit(0)
mqttClient.loop_start()

while not mqttClient.is_connected():
    print("Waiting for connection...")
    time.sleep(1)


mqttClient.publish("house/main/main-light", "on")
print("Message published")
mqttClient.loop_stop()
print("Disconnecting from the Broker", brokerAddress)
mqttClient.disconnect()
