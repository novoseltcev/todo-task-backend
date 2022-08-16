from flask import jsonify
from flask_jwt_extended import jwt_required

from app.rest_lib.controller import Controller
from app.utils.schemas import AuthSchema

from .service import JWTService, Tokens
from .schema import JWTSchema


class JWTController(Controller):
    service: JWTService

    def __init__(self):
        super().__init__(
            service=JWTService(),
            schema_builder=JWTSchema
        )

    def post(self):
        auth_data = AuthSchema().load(self.json)
        tokens: Tokens = self.service.create_tokens(auth_data)
        return jsonify(self.schema_builder().dump(tokens)), 201

    @jwt_required(refresh=True)
    def put(self):
        tokens: Tokens = self.service.refresh_access_token()
        return jsonify(self.schema_builder().dump(tokens)), 201

    @jwt_required(verify_type=False)
    def delete(self):
        self.service.revoke_token()
        return jsonify(), 204
