from flask_restful import Resource, abort, reqparse
from models.location import Location


def not_found(item):
    abort(404, error="404", message="{} not found".format(item))


parser = reqparse.RequestParser()
parser.add_argument('avail')

class LocationItem(Resource):
    def get(self, location_id):
        location_query = Location.query.filter(Location.id==location_id)
        if location_query.count() == 0:
            not_found('location')
        location_item = location_query.first()
        return location_item.serialize