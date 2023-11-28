from containers import Container
import seqlog as rootLogger
import sys
from dependency_injector.wiring import Provide, inject
from infrastructure.mqttclient import *


@inject
def main(
    mqtt_publisher: MqttPublisher.MqttPublisher = Provide[Container.mqtt_publisher],
    mqtt_subscriber: MqttSubscriber.MqttSubscriber = Provide[Container.mqtt_subscriber],
) -> None:
    def onmessage_callback(client, userdata, message):
        logger.info(
            "Received from topic %s message paylod: %s",
            message.topic,
            message.payload.decode("utf-8"),
        )

    rootLogger.configure_from_file("./seq.yml")
    logger = rootLogger.logging.getLogger()

    try:
        result = mqtt_publisher.publish("on")
        if not result:
            logger.warning(
                "Unable to publish message. If its quited, reduce log level to see details."
            )

    except Exception as ex:
        logger.error(ex)

    mqtt_client = MqttSubscriber.Client
    try:
        mqtt_client = mqtt_subscriber.subscribe_to_topic(
            "house/main/main-light", onmessage_callback=onmessage_callback
        )
        while mqtt_client.is_connected:
            pass

    except KeyboardInterrupt:
        logger.info("Application exiting")
        mqtt_subscriber.disconnect_from_broker()
        sys.exit(0)


# This block checks if the script is being run as the main program
if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])  # type: ignore
