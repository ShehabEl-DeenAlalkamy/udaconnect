# from multiprocessing import Process
# import threading
# import os
# import logging
# from kafka import KafkaConsumer
# from queue import Queue

# logger = logging.getLogger('kafka-consumer')
# logger.setLevel(logging.INFO)


# # def _process_msg(q, c):
# #     msg = q.get(timeout=60)  # Set timeout to care for POSIX<3.0 and Windows.
# #     logging.info(
# #         '#%sT%s - Received message: %s',
# #         os.getpid(), threading.get_ident(), msg.value().decode('utf-8')
# #     )
# #     time.sleep(5)
# #     q.task_done()
# #     c.commit(msg)


# # def _consume(config):
# #     logging.info(
# #         '#%s - Starting consumer group=%s, topic=%s',
# #         os.getpid(), config['kafka_kwargs']['group.id'], config['topic'],
# #     )
# #     c = Consumer(**config['kafka_kwargs'])
# #     c.subscribe([config['topic']])
# #     q = Queue(maxsize=config['num_threads'])

# #     while True:
# #         logging.info('#%s - Waiting for message...', os.getpid())
# #         try:
# #             msg = c.poll(60)
# #             if msg is None:
# #                 continue
# #             if msg.error():
# #                 logging.error(
# #                     '#%s - Consumer error: %s', os.getpid(), msg.error()
# #                 )
# #                 continue
# #             q.put(msg)
# #             # Use default daemon=False to stop threads gracefully in order to
# #             # release resources properly.
# #             t = threading.Thread(target=_process_msg, args=(q, c))
# #             t.start()
# #         except Exception:
# #             logging.exception('#%s - Worker terminated.', os.getpid())
# #             c.close()


# # def main(config):
# #     """
# #     Simple program that consumes messages from Kafka topic and prints to
# #     STDOUT.
# #     """
# #     workers = []
# #     while True:
# #         num_alive = len([w for w in workers if w.is_alive()])
# #         if config['num_workers'] == num_alive:
# #             continue
# #         for _ in range(config['num_workers']-num_alive):
# #             p = Process(target=_consume, daemon=True, args=(config,))
# #             p.start()
# #             workers.append(p)
# #             logging.info('Starting worker #%s', p.pid)


# class MessageConsumer():
#     broker = ""
#     topic = ""
#     producer = None

#     def __init__(self, broker, topic, workers_num=1, threads_num=1):
#         self.broker = broker
#         self.topic = topic
#         self.workers_num = workers_num
#         self.threads_num = threads_num
#         self.run_process = Process(target=self.__run(), daemon=True)
#         # self.run_process.start()
#         # Gives the thread an envent called stop_event so it can be interrupted.
#         # self.stop_event = multiprocessing.Event()

#     def start(self):
#         if not self.run_process.is_alive():
#             self.run_process.start()

#     def __run(self):
#         workers = []
#         print("__run() invoked")
#         while True:
#             live_num = len([worker for worker in workers if worker.is_alive()])

#             if self.workers_num == live_num:
#                 continue

#             for _ in range(self.workers_num - live_num):
#                 # p = Process(target=self.__consume(), daemon=True)
#                 p.start()
#                 workers.append(p)
#                 print('Starting worker #%s', p.pid)

#     def __consume(self):
#         print("__consume() invoked")
#         print('#%s - Starting consumer topic=%s', os.getpid(), self.topic)

#         consumer = KafkaConsumer(self.topic,
#                                  bootstrap_servers=self.broker,
#                                  group_id="my_group_id",
#                                  consumer_timeout_ms=1000,
#                                  value_deserializer=lambda v: v.decode(
#                                      'utf-8'),
#                                  enable_auto_commit=False)

#         queue = Queue(maxsize=self.threads_num)

#         print('#%s - Waiting for message...', os.getpid())
#         while True:
#             try:
#                 msg = consumer.poll(60)

#                 if msg is None:
#                     continue

#                 # if msg.error():
#                 #     print('#%s - Consumer error: %s', os.getpid(), msg.error())
#                 #     continue

#                 queue.put(msg)
#                 print(msg)

#                 # Use default daemon=False to stop threads gracefully in order to
#                 # release resources properly.
#                 # t = threading.Thread(target=self.__process(queue, consumer))
#                 # t.start()
#             except Exception as e:
#                 print(str(e))
#                 print('#%s - Worker terminated.', os.getpid())
#                 # consumer.close()

#     def __process(self, queue, consumer):
#         # Set timeout to care for POSIX<3.0 and Windows.
#         msg = queue.get(timeout=60)
#         print('#%sT%s - Received message: %s', os.getpid(),
#               threading.get_ident(), msg)
#         queue.task_done()
#         consumer.commit(msg)

#     # def stop(self):
#     #     self.stop_event.set()

#     # def run(self):
#     #     if hasattr(os, 'getppid'):  # only available on Unix
#     #         print(f"parent process: {os.getppid()}")
#     #         proc_id = os.getppid()

#     #     consumer = KafkaConsumer(self.topic,
#     #                              client_id=f"{self.topic}-consumer-{proc_id}",
#     #                              bootstrap_servers=self.broker,
#     #                              consumer_timeout_ms=1000,
#     #                              value_deserializer=lambda v: v.decode('utf-8'))

#     #     # loop until the thread is stopped by checking the stop event
#     #     while not self.stop_event.is_set():
#     #         for message in consumer:
#     #             logger.log(level=logging.INFO, msg=message)
#     #             # self.logger.info(
#     #             #     f"{self.topic}-consumer-{proc_id} processed message: {message.topic}:{message.offset} value={message.value}")
#     #             # break out of the for loop if the thread was notified of closure
#     #             if self.stop_event.is_set():
#     #                 break

#         # Close the TCP connection to kafka
#         # consumer.close()
