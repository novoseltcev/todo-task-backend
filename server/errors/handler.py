from server import app, jwt
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


@jwt.invalid_token_loader
def invalid_token_handler(jwt_header):
    return {"error": str(InvalidToken())}, 401


@jwt.expired_token_loader
def expired_token_handler(jwt_header, jwt_payload):
    return {"error": str(ExpiredToken())}, 401


@jwt.revoked_token_loader
def revoked_token_handler(jwt_header, jwt_payload):
    return {"error": str(TokenInBlockList())}, 401
