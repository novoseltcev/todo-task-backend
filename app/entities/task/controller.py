from flask import jsonify

from app.auth import auth_service
from app.models import Role

from app.rest_lib.controller import Controller
from .schema import TaskSchema
from .service import TaskService


class TaskController(Controller):
    service: TaskService

    def __init__(self):
        super().__init__(service=TaskService())

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self, task_id: int):
        entity = self.service.get_by_pk(user_id=self.user.id, entity_id=task_id)
        return jsonify(
            data=TaskSchema().dump(entity)
        ), 200

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def post(self):
        data = TaskSchema(exclude=('id', 'status')).load(self.json)
        return jsonify(
            id=self.service.create(user_id=self.user.id, data=data)
        ), 201

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def put(self, task_id: int):
        data = TaskSchema(exclude=('category_id', )).load(self.json)
        self.service.edit(user_id=self.user.id, entity_id=task_id, data=data)
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def patch(self, task_id: int):
        self.service.change_category(
            user_id=self.user.id,
            entity_id=task_id,
            category_id=TaskSchema(only=('category_id', )).load(self.json)['category_id']
        )
        return jsonify(), 204

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self, task_id: int):
        self.service.delete(user_id=self.user.id, entity_id=task_id)
        return jsonify(), 204
