import paho.mqtt.client as pahoClient
import uuid
import configparser as config


def on_connect(client, userData, flags, responseCode):
    match responseCode:
        case 0:
            print("MQTT Client connected")
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


brokerAddress = ""
mqttConnectionName = str.format("pinga-client-{0}", uuid.uuid4())
mqttClient = pahoClient.Client(mqttConnectionName)
mqttClient.on_connect = on_connect

print("Connecting to the Broker {0}", brokerAddress)
# mqttClient.tls_set()
# mqttClient.tls_insecure_set(True)
# mqttClient.username_pw_set("", "")
mqttClient.connect(brokerAddress, port=1883)
mqttClient.loop_start()
mqttClient.publish("house/main/main-light", "on")
mqttClient.loop_stop()
print("Disconnecting from the Broker {0}", brokerAddress)
mqttClient.disconnect()
