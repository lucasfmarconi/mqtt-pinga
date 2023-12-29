from logging import Logger
from math import e
from .MqttConnector import MqttConnector
import paho.mqtt.client as pahoClient
import seqlog as logging
import time
import yaml


class MqttPublisher:
    def __init__(self, logger: Logger, mqtt_connector: MqttConnector):
        self.logger = logger
        self.mqtt_connector = mqtt_connector

        with open("mqtt.yml", "r") as file:
            config = yaml.safe_load(file)

        self.broker_address = config["broker"]["host"]
        self.broker_port = config["broker"]["port"]
        pass

    def connect_to_broker(self) -> pahoClient.Client:
        mqtt_client = self.mqtt_connector.connect(self.broker_address, self.broker_port)
        self.logger.debug(
            "Starting mqtt broker connection to the %s host", self.broker_address
        )
        return mqtt_client

    def publish(self, payload: str) -> bool:
        mqtt_client = self.connect_to_broker()

        mqtt_client.loop_start()

        while not mqtt_client.is_connected():
            self.logger.debug("Waiting for CONNACK...")
            time.sleep(1)

        mqtt_client.publish("house/main/main-light", payload, qos=0, retain=True)
        self.logger.debug("Message published")
        mqtt_client.loop_stop()

        self.mqtt_connector.disconnect()
        return True
