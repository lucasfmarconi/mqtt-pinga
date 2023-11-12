from infrastructure.mqttclient import mqttClient
import seqlog as rootLogger
import sys
import time

rootLogger.configure_from_file("./seq.yml")
logger = rootLogger.logging.getLogger()

brokerAddress = "localhost"

logger.info("Connecting to the Broker %s", brokerAddress)
try:
    mqttClient.connect(brokerAddress, port=1883)
except:
    logger.error("Unable to connect to the broker %s", brokerAddress)
    sys.exit(0)
mqttClient.loop_start()

while not mqttClient.is_connected():
    logger.debug("Waiting for CONNACK...")
    time.sleep(1)


mqttClient.publish("house/main/main-light", "on")
logger.debug("Message published")
mqttClient.loop_stop()
logger.info("Disconnecting from the Broker %s", brokerAddress)
mqttClient.disconnect()