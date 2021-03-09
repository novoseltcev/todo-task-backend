from sqlalchemy.exc import IntegrityError

from server import app
from server.errors.exc import *


@app.errorhandler(CategoryExistName)
def integrity_error(err):
    return {"error": err.__str__()}, 403


@app.errorhandler(TaskUnknownId)
@app.errorhandler(CategoryUnknownId)
@app.errorhandler(FileUnknownId)
def id_error(err):
    return {"error": str(err)}, 404


@app.errorhandler(InvalidSchema)
def schema_error(err):
    return {"error": str(err)}, 422


@app.errorhandler(ForbiddenOperation)
def forbidden_error(err):
    return {"error": str(err)}, 401
