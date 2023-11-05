import sys
import time
import paho.mqtt.client as pahoClient
import uuid
import seqlog as logging

logging.configure_from_file("./seq.yml")
logger = logging.logging

def on_log(client, userdata, level, buf):
    logger.debug(buf)

def on_connect_fail(client, userData):
    logger.warning("Connection failed")

def on_connect(client, userData, flags, responseCode):
    match responseCode:
        case 0:
            logger.info("MQTT Client connected")
            return
        case 1:
            logger.warning(
                "The server does not support the MQTT protocol requested by the client"
            )
        case 2:
            logger.warning(
                "The client ID is the correct UTF-8 string, but is not allowed by the server"
            )
        case 3:
            logger.warning(
                "Network connection has been established, but MQTT service is unavailable"
            )
        case 4:
            logger.warning("The data in the username or password is in the wrong format")
        case 5:
            logger.warning("Client connection is not authorized")

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

logger.info("Connecting to the Broker %s", brokerAddress)
try:
    mqttClient.connect(brokerAddress, port=1883)
except:
    logger.error("Unable to connect to the broker %s", brokerAddress)
    sys.exit(0)
mqttClient.loop_start()

while not mqttClient.is_connected():
    logger.debug("Waiting for connection...")
    time.sleep(1)


mqttClient.publish("house/main/main-light", "on")
logger.debug("Message published")
mqttClient.loop_stop()
logger.info("Disconnecting from the Broker %s", brokerAddress)
mqttClient.disconnect()

