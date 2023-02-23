from app.config import _init_logger

from kafka import KafkaProducer
import json
import logging

_init_logger()
logger = logging.getLogger('udaconnect.locations_svc.kafka.producer')


class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        logger.info(f"opening {self} connection at {self.broker}")
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
                                      client_id=f"{self.topic}-producer",
                                      value_serializer=lambda v: json.dumps(
                                          v).encode('utf-8'),
                                      acks='all',
                                      retries=3)

    def send_msg(self, msg):
        error = None
        try:
            self.producer.send(self.topic, msg)
            self.producer.flush()
            logger.info(f"message=\"{msg}\" sent successfully..")
        except Exception as e:
            logger.error(
                f"error: unable to send message=\"{msg}\" reason=\"{str(e)}\"")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return error

    def __str__(self) -> str:
        return f"{self.topic}-producer"

    def __del__(self):
        logger.info(f"closing {self} connection..")
        self.producer.close()
