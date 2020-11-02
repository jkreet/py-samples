from app import app
from app import api

from resources.car_item import CarItem
from resources.car_list import CarList
from resources.model_item import ModelItem
from resources.model_list import ModelList
from resources.location_item import LocationItem

api.add_resource(ModelList, '/models')
api.add_resource(ModelItem, '/models/<model_id>')
api.add_resource(CarList, '/cars')
api.add_resource(CarItem, '/cars/<car_id>')
api.add_resource(LocationItem, '/locations/<location_id>')

if __name__ == '__main__':
    app.run()