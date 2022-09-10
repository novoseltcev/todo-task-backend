from flask import jsonify

from app.rest_lib.controller import Controller
from app.models import Role
from app.auth import auth_service

from .schema import CategorySchema
from .service import CategoryService


class CategoryController(Controller):
    service: CategoryService

    def __init__(self):
        super(CategoryController, self).__init__(service=CategoryService())

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self, category_id: id = None):
        if category_id:
            entity = self.service.get_by_pk(user_id=self.user.id, entity_id=category_id)
            return jsonify(
                data=CategorySchema().dump(entity)
            ), 200

        entities = self.service.get_by_user(user_id=self.user.id)
        return jsonify(
            data=CategorySchema(many=True, exclude=('tasks',)).dump(entities)
        ), 200

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def post(self):
        data = CategorySchema().load(self.json)
        return jsonify(
            id=self.service.create(user_id=self.user.id, data=data)
        ), 201

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def put(self, category_id: int):
        data = CategorySchema().load(self.json)
        self.service.edit(user_id=self.user.id, entity_id=category_id, data=data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self, category_id: int):
        self.service.delete(user_id=self.user.id, entity_id=category_id)
        return jsonify(), 204
