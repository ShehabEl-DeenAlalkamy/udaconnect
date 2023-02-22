from kafka import KafkaConsumer
import threading
import logging
import json
import os


class MessageConsumer(threading.Thread):
    broker = ""
    topic = ""

    def __init__(self, broker, topic, app, group_id="outlaw_group"):
        self.broker = broker
        self.topic = topic
        self.app = app
        self.group_id = group_id
        threading.Thread.__init__(self)

    def run(self):
        with self.app.app_context():
            from app.udaconnect.services import LocationService
            from app.udaconnect.schemas import LocationSchema
            from app.udaconnect.models import Location
            from app.config import _init_logger

            _init_logger()
            logger = logging.getLogger(
                'udaconnect.locations_svc.kafka.consumer')

            logger.info(
                f"#%{os.getpid()} T{threading.get_ident()} - starting consumer topic={self.topic} broker={self.broker}")

            consumer = KafkaConsumer(self.topic,
                                     bootstrap_servers=self.broker,
                                     group_id=self.group_id,
                                     consumer_timeout_ms=1000,
                                     value_deserializer=lambda v: json.loads(v.decode('utf-8')))

            while True:
                try:
                    for message in consumer:
                        if message is None:
                            continue

                        logger.info(
                            f"#{os.getpid()} T{threading.get_ident()} - received message: topic={message.topic} value={message.value} partition={message.partition} offset={message.offset} timestamp={message.timestamp}")
                        logger.info(
                            f"#{os.getpid()} T{threading.get_ident()} - processing..")

                        message_action = message.value['action']
                        message_content = message.value['data']

                        try:
                            if message_action == "create":
                                location = dict()
                                logger.info(
                                    f"#{os.getpid()} T{threading.get_ident()} - action='{message_action}', creating new 'Location' resource..")

                                location: Location = LocationService.create(
                                    message_content)
                                if not location:
                                    logger.error(
                                        f"#{os.getpid()} T{threading.get_ident()} - unable to create 'Location' resource")

                                else:
                                    logger.info(
                                        f"#{os.getpid()} T{threading.get_ident()} - created location={LocationSchema().dump(location)}")
                                    logger.info(
                                        f"#{os.getpid()} T{threading.get_ident()} - successfully finished processing")
                            elif message_action == "delete":
                                location = dict()
                                logger.info(
                                    f"#{os.getpid()} T{threading.get_ident()} - action='{message_action}', deleting 'Location' resource..")
                            else:
                                logger.exception(
                                    f"#{os.getpid()} T{threading.get_ident()} - expected action='create' got '{message_action}' instead")
                                logger.info(
                                    f"#{os.getpid()} T{threading.get_ident()} - nothing to do..")

                        except Exception as e:
                            logger.exception(
                                f"#{os.getpid()} T{threading.get_ident()} - error: {str(e)}")

                except Exception as e:
                    logger.exception(
                        f"#%{os.getpid()} T{threading.get_ident()} - worker terminated reason={str(e)}")
                    consumer.close()
