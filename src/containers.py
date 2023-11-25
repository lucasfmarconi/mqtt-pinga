import seqlog
from logging import Logger
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from infrastructure.mqttclient import MqttPublisher, MqttSubscriber, MqttConnector


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    seqlog.configure_from_file("./seq.yml")

    logger = providers.Singleton(Logger, seqlog.logging.getLogger())

    mqtt_connector = providers.Factory(MqttConnector.MqttConnector, logger)
