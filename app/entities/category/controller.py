from flask import jsonify

from app.rest_lib.controller import Controller
from app.models import Role
from app.auth import auth_service

from .schema import CategorySchema
from .service import CategoryService


class CategoryController(Controller):
    service: CategoryService

    def __init__(self):
        super(CategoryController, self).__init__(
            service=CategoryService(),
            schema_builder=CategorySchema
        )

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self, name: str = None):
        if name:
            entity = self.service.get_by_pk(user_id=self.user.id, name=name)
            return self.schema_builder().dump(entity), 200

        entities = self.service.get_by_user(user_id=self.user)
        return self.schema_builder(many=True).dump(entities), 200

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def post(self):
        data = self.schema_builder().load(self.json)
        entity = self.service.create(user_id=self.user.id, data=data)
        return self.schema_builder().dump(entity), 201

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def put(self, name: str):
        data = self.schema_builder().load(self.json)
        self.service.edit(user_id=self.user.id, name=name, data=data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self, name: str):
        self.service.delete(user_id=self.user.id, name=name)
        return jsonify(), 204
