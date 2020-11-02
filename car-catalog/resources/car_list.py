from flask_restful import Resource, abort, reqparse
from models.car import Car

def not_found(item):
    abort(404, error="404", message="{} not found".format(item))


parser = reqparse.RequestParser()
parser.add_argument('avail')

class CarList(Resource):
    def get(self):
        args = parser.parse_args()

        if args['avail']:
            avail = 1 if str.lower(args['avail']) == 'true' else 0
            cars_query = Car.query.filter(Car.avail == avail)
        else:
            cars_query = Car.query

        if cars_query.count() == 0:
            not_found('cars')

        cars = cars_query.all()

        car_list = []
        for car in cars:
            car_list.append(car.serialize)

        return car_list