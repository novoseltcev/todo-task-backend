from flask import Blueprint
from server import jwt
from server.errors import exc

error_blueprint = Blueprint('errors', __name__)


@error_blueprint.app_errorhandler(exc.CategoryExistName)
def integrity_error(err):
    return {"error": err.__str__()}, 403


@error_blueprint.app_errorhandler(exc.TaskUnknownId)
@error_blueprint.app_errorhandler(exc.CategoryUnknownId)
@error_blueprint.app_errorhandler(exc.FileUnknownId)
def id_error(err):
    return {"error": str(err)}, 404


@error_blueprint.app_errorhandler(exc.InvalidSchema)
def schema_error(err):
    return {"error": str(err)}, 422


@error_blueprint.app_errorhandler(exc.UnconfirmedEmailError)
@error_blueprint.app_errorhandler(exc.ForbiddenOperation)
def forbidden_error(err):
    return {"error": str(err)}, 401


@error_blueprint.app_errorhandler(exc.NoContentError)
def no_content_handler(err):
    return {'msg': str(exc.NoContentError)}, 204


@jwt.invalid_token_loader
def invalid_token_handler(jwt_header):
    return {"error": str(exc.InvalidToken())}, 401


@jwt.expired_token_loader
def expired_token_handler(jwt_header, jwt_payload):
    return {"expired_error": str(exc.ExpiredToken())}, 401


@jwt.revoked_token_loader
def revoked_token_handler(jwt_header, jwt_payload):
    return {"error": str(exc.TokenInBlockList())}, 401
