from flask_restful import Resource, abort, reqparse
from models.car import Car

def not_found(item):
    abort(404, error="404", message="{} not found".format(item))


parser = reqparse.RequestParser()
parser.add_argument('avail')

class CarItem(Resource):
    def get(self, car_id):
        car_query = Car.query.filter(Car.id==car_id)
        if car_query.count() == 0:
            not_found('car')
        car_item = car_query.first()
        return car_item.serialize
