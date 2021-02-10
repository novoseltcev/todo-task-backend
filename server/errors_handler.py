from sqlalchemy.exc import IntegrityError

from server import app


@app.errorhandler(KeyError)
def invalid_request_error(error):
    return {"error": "Invalid request"}, 400


@app.errorhandler(ValueError)
def value_error(error):
    return error.args[0], 404


@app.errorhandler(IntegrityError)
def integrity_error(error):
    return {"error": "value already exists"}, 403
