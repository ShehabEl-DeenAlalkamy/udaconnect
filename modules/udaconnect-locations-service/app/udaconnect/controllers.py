from app import _logger
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService

from flask import request, Response, g
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
import json


api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        error = g.kafka_producer.send_msg({
            'action': "create",
            'data': request.get_json()
        })
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')

        return Response(status=202, mimetype='application/json')

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location, error = LocationService.retrieve(location_id)
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')
        return location

    @responds(schema=LocationSchema)
    def delete(self, location_id) -> None:
        _, error = LocationService.retrieve(location_id)
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')

        error = g.kafka_producer.send_msg({
            'action': "delete",
            'data': {
                'id': location_id
            }
        })
        if error:
            return Response(response=json.dumps({'error': error['message']}), status=error['status_code'], mimetype='application/json')

        return Response(status=202, mimetype='application/json')
