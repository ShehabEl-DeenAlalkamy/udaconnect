from app import db
from app import _logger
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema

from typing import Dict
from geoalchemy2.functions import ST_Point
from sqlalchemy.orm import exc


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location = None
        error = None
        try:
            location, coord_text = (
                db.session.query(Location, Location.coordinate.ST_AsText())
                .filter(Location.id == location_id)
                .one()
            )

            # Rely on database to return text form of point to reduce overhead of conversion in app code
            location.wkt_shape = coord_text

        except exc.NoResultFound:
            _logger.exception(
                f"error: NoResultFound for location_id={location_id}")
            error = {
                'status_code': 404,
                'message': "Resource not found."
            }
        except Exception as e:
            _logger.exception(
                f"error: unable to fetch location_id={location_id} reason={str(e)}")
            error = {
                'status_code': 500,
                'message': "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
            }
        return location, error

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            _logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(
            location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        return new_location
