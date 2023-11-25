from logging import Logger
import paho.mqtt.client as pahoClient
import uuid
import seqlog as logging


class MqttConnector:
    broker_host: str

    def __init__(self, logger: Logger):
        if logger is None:
            logging.configure_from_file("./seq.yml")
            self.logger = logging.logging.getLogger("mqttConn")
            pass

        self.logger = logger
        pass

    def on_log(self, client, userdata, level, buf):
        self.logger.debug(buf)

    def on_connect_fail(self, client, userData):
        self.logger.warning("Connection failed")

    def on_connect(self, client, userData, flags, responseCode):
        match responseCode:
            case 0:
                self.logger.info("MQTT Client connected")
                return
            case 1:
                self.logger.warning(
                    "The server does not support the MQTT protocol requested by the client"
                )
            case 2:
                self.logger.warning(
                    "The client ID is the correct UTF-8 string, but is not allowed by the server"
                )
            case 3:
                self.logger.warning(
                    "Network connection has been established, but MQTT service is unavailable"
                )
            case 4:
                self.logger.warning(
                    "The data in the username or password is in the wrong format"
                )
            case 5:
                self.logger.warning("Client connection is not authorized")

        if responseCode != 0:
            client.loop_stop()

    def connect(
        self,
        host: str,
        port: int,
        connectionName=str.format("pinga-client-{0}", uuid.uuid4()),
    ):
        self.logger.debug(
            "Client %s is connecting to the broker %s : %s", connectionName, host, port
        )
        self.broker_host = connectionName
        self.mqttClient = pahoClient.Client(connectionName)
        self.mqttClient.connect(host, port)
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_connect_fail = self.on_connect_fail
        self.mqttClient.on_log = self.on_log
        return self.mqttClient

    def disconnect(self):
        self.logger.info("Disconnecting from the Broker '%s'", self.broker_host)
        self.mqttClient.disconnect()
