#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import flask
from flask import request
from models.OrgUnit import OrgUnit
from models.User import User


app = flask.Flask(__name__)


# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def to_json(data):
    return json.dumps(data, ensure_ascii=False) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json; charset=utf-8",
        response=to_json(data)
    )


# def theme_validate():
#     errors = []
#     json = flask.request.get_json()
#     if json is None:
#         errors.append(
#             "No JSON sent. Did you forget to set Content-Type header" +
#             " to application/json?")
#         return (None, errors)
#
#     for field_name in ['title', 'url']:
#         if type(json.get(field_name)) is not str:
#             errors.append(
#                 "Field '{}' is missing or is not a string".format(
#           field_name))
#
#     return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/users')


# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})


@app.route('/api/1.0/users/', methods=['GET'])
def get_users():
    users = User.find()

    return resp(200, users)

@app.route('/api/1.0/users/<username>', methods=['GET'])
def get_user(username):
    renew = request.args.get('renew')
    user =  User.find(username, renew)

    if not user:
        return resp(404, "Not found")

    return resp(200, user)

@app.route('/api/1.0/org_units/', methods=['GET'])
def get_org_units():
    org_units = OrgUnit.find()
    return resp(200, org_units)

@app.route('/api/1.0/heartbit/', methods=['GET'])
def return_heartbit():
    return resp(200, 'im ok now!')



#if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = True
    app.debug = True  # enables auto reload during development
    app.run(host='0.0.0.0', port=8080)
