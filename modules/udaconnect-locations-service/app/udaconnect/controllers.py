from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from app.udaconnect.utils import send_data
from flask import request, Response, g, current_app
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        status_code = 202
        res = None

        err = g.kafka_producer.send_msg({
            'action': "create",
            'data': request.get_json()
        })

        if err:
            current_app.logger.error(f"Error: {str(err)}")
            status_code = 500
            res = "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."

        return Response(response=res, status=status_code, mimetype='application/json')

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location
