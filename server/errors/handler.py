from flask import Blueprint
from server import jwt
from server.errors.exc import *

error_blueprint = Blueprint('errors', __name__)


@error_blueprint.errorhandler(CategoryExistName)
def integrity_error(err):
    return {"error": err.__str__()}, 403


@error_blueprint.errorhandler(TaskUnknownId)
@error_blueprint.errorhandler(CategoryUnknownId)
@error_blueprint.errorhandler(FileUnknownId)
def id_error(err):
    return {"error": str(err)}, 404


@error_blueprint.errorhandler(InvalidSchema)
def schema_error(err):
    return {"error": str(err)}, 422


@error_blueprint.errorhandler(ForbiddenOperation)
def forbidden_error(err):
    return {"error": str(err)}, 401


@error_blueprint.errorhandler(NoContentError)
def no_content_handler(err):
    return {'msg': str(NoContentError)}, 204


@jwt.invalid_token_loader
def invalid_token_handler(jwt_header):
    return {"error": str(InvalidToken())}, 401


@jwt.expired_token_loader
def expired_token_handler(jwt_header, jwt_payload):
    return {"expired_error": str(ExpiredToken())}, 401


@jwt.revoked_token_loader
def revoked_token_handler(jwt_header, jwt_payload):
    return {"error": str(TokenInBlockList())}, 401
