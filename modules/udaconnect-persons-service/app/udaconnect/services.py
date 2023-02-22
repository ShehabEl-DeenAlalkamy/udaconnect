from app import db
from app import _logger
from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from typing import Dict, List
from sqlalchemy.orm import exc


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        validation_results: Dict = PersonSchema().validate(person)
        if validation_results:
            _logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        try:
            db.session.add(new_person)
            db.session.commit()
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
            raise Exception from e

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = None
        error = None
        try:
            person = db.session.query(Person).get(person_id)
            if bool(person):
                _logger.info(f"found person={PersonSchema().dump(person)}")
            else:
                _logger.exception(
                    f"error: NoResultFound for person_id={person_id}")
                error = {
                    'status_code': 404,
                    'message': "Resource not found."
                }
        except exc.NoResultFound:
            _logger.exception(
                f"error: NoResultFound for person_id={person_id}")
            error = {
                'status_code': 404,
                'message': "Resource not found."
            }
        except Exception as e:
            _logger.exception(
                f"error: unable to fetch person_id={person_id} reason={str(e)}")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return person, error

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()
