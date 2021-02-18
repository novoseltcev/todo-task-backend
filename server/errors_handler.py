from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from server import app


# @app.errorhandler(ValueError)
def value_error(error):
    return error.args[0], 403


@app.errorhandler(IntegrityError)
def integrity_error(error):
    return {"error": "value already exists"}, 403


@app.errorhandler(ValidationError)
def validation_error(err):
    return err.args[0], 422
