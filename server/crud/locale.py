from flask import request
from server import flask_app
from server.handler import *


def preset_json_receive_method(func):
    def wrapper():
        json = request.json
        try:
            return func(json)
        except KeyError:
            return raise_error("Invalid request")
    return wrapper
