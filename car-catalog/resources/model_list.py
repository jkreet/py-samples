from flask_restful import Resource, abort, reqparse
from models.car_model import Model


def not_found(item):
    abort(404, error="404", message="{} not found".format(item))

class ModelList(Resource):
    def get(self):
        model_query = Model.query

        if model_query.count() == 0:
            not_found('models')

        models = model_query.all()

        model_list = []
        for model in models:
            model_list.append(model.serialize)

        return model_list
