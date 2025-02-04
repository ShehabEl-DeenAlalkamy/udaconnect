from app.udaconnect.models import Person
from app.udaconnect.schemas import PersonSchema
from app.udaconnect.services import PersonService

from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
import json

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person, error = PersonService.create(payload)
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons, error = PersonService.retrieve_all()
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')
        return persons


# TODO: implement DELETE /persons/<person_id> --> don't forget to delete person locations records
@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person, error = PersonService.retrieve(person_id)
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')
        return person
