from app.udaconnect.services import LocationService
from app.udaconnect.models import Location
from multiprocessing import Process
from kafka import KafkaConsumer
from queue import Queue
import threading
import os
import logging
import time


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger('udaconnect.locations_svc.kafka.consumer')


class MessageConsumer():
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic, workers_num=2, threads_num=1, group_id="outlaw_group"):
        self.broker = broker
        self.topic = topic
        self.workers_num = workers_num
        self.threads_num = threads_num
        self.group_id = group_id
        self.run_process = Process(target=self.run, daemon=False)

    def start(self):
        if not self.run_process.is_alive():
            self.run_process.start()

    def run(self):
        workers = []
        while True:
            live_num = len([worker for worker in workers if worker.is_alive()])

            if self.workers_num == live_num:
                continue

            for _ in range(self.workers_num - live_num):
                p = Process(target=self.consume, daemon=True)
                p.start()
                workers.append(p)
                logger.info(f"starting worker #{p.pid}")

    def consume(self):
        logger.info(
            f"#%{os.getpid()} - starting consumer topic={self.topic} broker={self.broker}")

        consumer = KafkaConsumer(self.topic,
                                 bootstrap_servers=self.broker,
                                 group_id=self.group_id,
                                 consumer_timeout_ms=1000,
                                 value_deserializer=lambda v: v.decode('utf-8'))

        queue = Queue(maxsize=self.threads_num)

        logger.info(f"#%{os.getpid()} - waiting for messages..")
        while True:
            try:
                for message in consumer:
                    if message is None:
                        continue

                    if queue.full():
                        logger.info(
                            "maximum threads reached, waiting for idle workers..")
                        continue

                    queue.put(message)

                    # Use default daemon=False to stop threads gracefully in order to
                    # release resources properly.
                    t = threading.Thread(
                        target=self.process_msg, args=(queue, consumer))
                    t.start()
            except Exception as e:
                logger.exception(
                    f"#%{os.getpid()} - worker terminated reason={str(e)}")
                consumer.close()

    def process_msg(self, queue, consumer):
        # Set timeout to care for POSIX<3.0 and Windows.
        msg = queue.get(timeout=60)

        logger.info(f"#{os.getpid()} T{threading.get_ident()} - received message: topic={msg.topic} value={msg.value} partition={msg.partition} offset={msg.offset} timestamp={msg.timestamp}")
        logger.info(f"#{os.getpid()} T{threading.get_ident()} - processing..")

        message_action = msg.value['action']
        message_content = msg.value['data']

        try:
            if message_action == "create":
                location = None
                logger.info(
                    f"#{os.getpid()} T{threading.get_ident()} - action={message_action}, creating new 'Location' resource..")
                location: Location = LocationService.create(message_content)
                logger.info(
                    f"#{os.getpid()} T{threading.get_ident()} - location={location}")

        except Exception as e:
            logger.exception(
                f"#{os.getpid()} T{threading.get_ident()} - error: {str(e)}")
