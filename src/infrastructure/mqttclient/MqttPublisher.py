from math import e
from .MqttConnector import MqttConnector
import seqlog as logging
import time
import yaml


class MqttPublisher:
    def __init__(self, logger):
        if logger is None:
            logging.configure_from_file("./seq.yml")
            logger = logging.logging.getLogger("mqttConn")

        self.logger = logger
        self.connector = MqttConnector(logger=logger)

        with open("mqtt.yml", "r") as file:
            config = yaml.safe_load(file)

        broker_address = config["broker"]["host"]
        broker_port = config["broker"]["port"]

        return self.connect_to_broker(broker_address, broker_port)

    def connect_to_broker(self, broker_address, broker_port):
        try:
            self.mqtt_client = self.connector.connect(broker_address, broker_port)
            self.logger.debug(
                "Starting mqtt broker connection to the %s host", broker_address
            )
            pass

        except Exception as ex:
            self.logger.error("Unable to connect to the broker %s", broker_address)
            return ex

    def publish(self, payload: str) -> bool:
        self.mqtt_client.loop_start()

        while not self.mqtt_client.is_connected():
            self.logger.debug("Waiting for CONNACK...")
            time.sleep(1)

        self.mqtt_client.publish("house/main/main-light", payload)
        self.logger.debug("Message published")
        self.mqtt_client.loop_stop()

        self.connector.disconnect()
        return True
