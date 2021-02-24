from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from server import app


@app.errorhandler(ValueError)
def value_error(error):
    return error.args[0], 403


@app.errorhandler(IntegrityError)
def integrity_error(error):
    return {"error": "value already exists"}, 422


@app.errorhandler(NoResultFound)
@app.errorhandler(ValidationError)
def validation_error(err):
    return {"error": err.args[0]}, 422
