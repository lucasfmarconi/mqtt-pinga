from cgi import test
import logging
from infrastructure.mqttclient import MqttPublisher
from infrastructure.mqttclient import MqttSubscriber
import seqlog as rootLogger
import sys


def onmessage_callback(client, userdata, message):
    logger.info(
        "Received from topic %s message paylod: %s",
        message.topic,
        message.payload.decode("utf-8"),
    )


rootLogger.configure_from_file("./seq.yml")
logger = rootLogger.logging.getLogger()

mqttPublisher = MqttPublisher.MqttPublisher(logger)

try:
    result = mqttPublisher.publish("on")
    if not result:
        logger.warning(
            "Unable to publish message. If its quited, reduce log level to see details."
        )

except Exception as ex:
    logger.error(ex)


subscriber = MqttSubscriber.MqttSubscriber(logger)
mqtt_client = MqttSubscriber.Client
try:
    mqtt_client = subscriber.subscribe_to_topic(
        "house/main/main-light", onmessage_callback=onmessage_callback
    )
    while mqtt_client.is_connected:
        pass

except KeyboardInterrupt:
    logger.info("Application exiting")
    subscriber.disconnect_from_broker()
    sys.exit(0)
