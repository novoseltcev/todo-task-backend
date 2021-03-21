from flask import redirect

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


@jwt.unauthorized_loader
def unauthorized_handler(jwt_header):
    return redirect('/login')
