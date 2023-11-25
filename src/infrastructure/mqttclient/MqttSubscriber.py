from logging import Logger
from math import e
from multiprocessing.connection import Client
from .MqttConnector import MqttConnector
import paho.mqtt.client as pahoClient
import yaml
import time


class MqttSubscriber:
    def __init__(self, logger: Logger, connector: MqttConnector):
        self.logger = logger
        self.connector = connector

        with open("mqtt.yml", "r") as file:
            config = yaml.safe_load(file)

        self.broker_address = config["broker"]["host"]
        self.broker_port = config["broker"]["port"]
        pass

    def connect_to_broker(self) -> pahoClient.Client:
        mqtt_client = self.connector.connect(self.broker_address, self.broker_port)
        self.logger.debug(
            "Starting mqtt broker connection to the %s host", self.broker_address
        )
        return mqtt_client

    def disconnect_from_broker(self):
        self.connector.disconnect()
        self.logger.debug(
            "Subscriber is disconnecting from the broker %s host", self.broker_address
        )

    def subscribe_to_topic(self, topic, onmessage_callback) -> pahoClient.Client:
        mqtt_client = self.connect_to_broker()
        mqtt_client.loop_start()
        mqtt_client.on_message = onmessage_callback

        while not mqtt_client.is_connected():
            self.logger.debug("Waiting for CONNACK...")
            time.sleep(1)

        mqtt_client.subscribe(topic)
        return mqtt_client
