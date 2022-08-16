from flask import jsonify

from app.auth import auth_service
from app.models import Role

from app.rest_lib.controller import Controller
from .schema import TaskSchema
from .service import TaskService


class TaskController(Controller):
    service: TaskService

    def __init__(self):
        super().__init__(
            service=TaskService(),
            schema_builder=TaskSchema
        )

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self, task_id: int):
        entity = self.service.get_by_pk(user_id=self.user.id, entity_id=task_id)
        return self.schema_builder().dump(entity), 200

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def post(self):
        data = self.schema_builder(exclude=('id', 'status')).load(self.json)
        entity = self.service.create(user_id=self.user.id, data=data)
        return self.schema_builder().dump(entity), 201

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def put(self, task_id: int):
        data = self.schema_builder(exclude=('category_id', )).load(self.json)
        self.service.edit(user_id=self.user.id, entity_id=task_id, data=data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def patch(self, task_id: int):
        category_name = self.schema_builder(only=('category_name', )).load(self.json)['category_name']
        self.service.change_category(user_id=self.user.id, entity_id=task_id, category_name=category_name)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self, task_id: int):
        self.service.delete(user_id=self.user.id, entity_id=task_id)
        return jsonify(), 204
