from infrastructure.mqttclient import MqttPublisher
import seqlog as rootLogger
import sys

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

sys.exit(0)
