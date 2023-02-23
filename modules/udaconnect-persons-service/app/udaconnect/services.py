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
        error = None
        try:
            db.session.add(new_person)
            db.session.commit()
            _logger.info(
                f"created new person={PersonSchema().dump(new_person)}")
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                _logger.error(
                    "IntegrityError: a Person with the same id already exists")
                error = {
                    "status_code": 400,
                    "message": "Bad Request: retry again may solve the problem"
                }
            else:
                _logger.error(
                    f"IntegrityError: unable to create 'Person' reason=\"{str(e)}\"")
                error = {
                    'status_code': 500,
                    'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
                }
        except Exception as e:
            _logger.error(
                f"error: unable to create 'Person' reason=\"{str(e)}\"")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return new_person, error

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = None
        error = None
        try:
            person = db.session.query(Person).get(person_id)
            if bool(person):
                _logger.info(f"found person={PersonSchema().dump(person)}")
            else:
                _logger.error(
                    f"error: NoResultFound for person_id={person_id}")
                error = {
                    'status_code': 404,
                    'message': "Resource not found."
                }
        except exc.NoResultFound:
            _logger.error(
                f"error: NoResultFound for person_id={person_id}")
            error = {
                'status_code': 404,
                'message': "Resource not found."
            }
        except Exception as e:
            _logger.error(
                f"error: unable to fetch person_id={person_id} reason=\"{str(e)}\"")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return person, error

    @staticmethod
    def retrieve_all() -> List[Person]:
        persons = []
        error = None
        try:
            persons = db.session.query(Person).all()
            _logger.info(f"found {len(persons)} persons")
        except Exception as e:
            _logger.error(
                f"error: unable to fetch persons reason=\"{str(e)}\"")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return persons, error
