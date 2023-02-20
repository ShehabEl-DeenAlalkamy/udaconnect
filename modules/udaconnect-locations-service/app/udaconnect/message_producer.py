from kafka import KafkaProducer
import json
from flask import current_app


class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic, logger=None):
        self.broker = broker
        self.topic = topic
        self.logger = logger or current_app.logger
        self.logger.info(f"opening Kafka connection at {self.broker}")
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
                                      value_serializer=lambda v: json.dumps(
                                          v).encode('utf-8'),
                                      acks='all',
                                      retries=3)

    def send_msg(self, msg):
        res = None
        try:
            self.producer.send(self.topic, msg)
            self.producer.flush()
            self.logger.info(f"message: {msg} sent successfully..")
        except Exception as e:
            res = e
        return res

    def __del__(self):
        self.logger.info("closing Kafka connection..")
        self.producer.close()
