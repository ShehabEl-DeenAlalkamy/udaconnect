from app.udaconnect.grpc.proto import person_pb2_grpc as pb2_grpc
from app.udaconnect.grpc.services.person_service import PersonService
from app.config import _init_logger

from concurrent import futures
import grpc
import logging

_init_logger()
_logger = logging.getLogger('udaconnect.persons_svc.grpc.server')


class Server:
    def __init__(self, app, port, address='[::]', max_workers=2):
        self.app = app
        self.address = address
        self.port = port
        self.max_workers = max_workers
        self.__server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers))

    def serve(self):
        # TODO: handle possible exceptions
        pb2_grpc.add_PersonServiceServicer_to_server(
            PersonService(self.app), self.__server)
        _logger.info(f"gRPC server running on {self.address}:{self.port}")
        self.__server.add_insecure_port(f"{self.address}:{self.port}")
        self.__server.start()

    def stop(self):
        _logger.info("shutting down gRPC server gracefully")
        self.__server.stop(3)
