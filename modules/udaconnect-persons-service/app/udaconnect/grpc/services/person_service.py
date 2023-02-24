from app.udaconnect.grpc.proto import person_pb2_grpc as pb2_grpc
from app.udaconnect.grpc.proto import person_pb2 as pb2


class PersonService(pb2_grpc.PersonServiceServicer):
    def __init__(self, app):
        self.app = app
        pb2_grpc.PersonServiceServicer.__init__(self)

    def ListPersons(self, request, context):
        with self.app.app_context():
            from app.udaconnect.schemas import PersonSchema
            from app.udaconnect import services as app_services
            from app.config import _init_logger
            import logging

            _init_logger
            logger = logging.getLogger(
                'udaconnect.persons_svc.grpc.server.person_svc')

            persons, _ = app_services.PersonService.retrieve_all()

            logger.info(f"received {len(persons)} persons from main server")
            logger.info(f"sending back to client..")

            return pb2.PersonMessageList(persons=[pb2.PersonMessage(**PersonSchema().dump(person)) for person in persons])
