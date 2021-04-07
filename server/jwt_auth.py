from functools import wraps

from flask import redirect, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from server import jwt, jwt_redis_blocklist


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.user_identity_loader
def user_identity_handler(user):
    try:
        return user.id
    except AttributeError:
        return user


# @jwt.unauthorized_loader
# def unauthorized_handler(jwt_header):
#     return redirect('/login')


def admin_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims('role', 0) in roles:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg=" ".join(x.upper() for x in roles) + " only!"), 403
        return decorator
    return wrapper
