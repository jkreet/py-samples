from flask_restful import Resource, abort, reqparse
from models.car_model import Model


def not_found(item):
    abort(404, error="404", message="{} not found".format(item))


parser = reqparse.RequestParser()
parser.add_argument('avail')

class ModelItem(Resource):
    def get(self, model_id):
        model_query = Model.query.filter(Model.id==model_id)
        if model_query.count() == 0:
            not_found('model')
        model_item = model_query.first()
        return model_item.serialize