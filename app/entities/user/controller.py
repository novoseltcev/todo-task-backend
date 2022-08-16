from flask import jsonify

from app.rest_lib.controller import Controller
from app.auth import auth_service
from .model import Role

from .service import UserService
from .schema import UserSchema


class UserController(Controller):
    service: UserService

    def __init__(self):
        super().__init__(
            service=UserService(),
            schema_builder=UserSchema
        )

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self):
        return jsonify(self.schema_builder().dump(self.user)), 200

    def post(self):
        data = self.schema_builder(only=('email', 'password')).load(self.json)
        self.service.register(**data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def put(self):
        data = self.schema_builder().load(self.json)
        self.service.edit(entity_id=self.user.id, data=data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self):
        self.service.delete(entity_id=self.user.id)
        return jsonify(), 204
