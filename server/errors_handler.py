from server import flask_app
from sqlite3 import IntegrityError


@flask_app.errorhandler(KeyError)
def invalid_request_error(error):
    return {"error": "Invalid request"}, 400


# @flask_app.errorhandler(ValueError)
def value_error(error):
    return error.args[0], 404


@flask_app.errorhandler(IntegrityError)
def integrity_error(error):
    return {"error": "value already exists"}, 403
