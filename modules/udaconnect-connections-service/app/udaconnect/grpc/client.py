from app.udaconnect.grpc.proto import person_pb2_grpc as pb2_grpc
from app.udaconnect.grpc.proto import person_pb2 as pb2
from app.config import _init_logger

import grpc
import logging

_init_logger()


class PersonStub:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__logger = logging.getLogger(
            'udaconnect.persons_svc.grpc.person_stub')

    def get_persons(self):
        persons = []

        self.__logger(
            f"instantiating secure channel with {self.host}:{self.port}")

        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = pb2_grpc.PersonServiceStub(channel)
            persons = stub.ListPersons(pb2.EmptyMessage())['persons']
            self.__logger(f"received {len(persons)} persons")
            self.__logger("closing channel..")

        return persons
