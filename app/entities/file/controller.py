from uuid import UUID

from flask import jsonify

from app.rest_lib.controller import Controller
from app.auth import auth_service
from app.models import Role

from .schema import FileSchema
from .service import FileService


class FileController(Controller):
    service: FileService

    def __init__(self):
        super(FileController, self).__init__(
            service=FileService()
        )

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def get(self, uuid: UUID):
        file = self.service.get_by_pk(uuid=uuid, user_id=self.user.id)
        return jsonify(
            data=FileSchema().dump(file)
        ), 200

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def post(self):
        data = FileSchema().load(self.json)
        file = self.service.create(user_id=self.user.id, **data)
        return jsonify(
            data=FileSchema().dump(file)
        ), 201

    @auth_service.allowed_roles(roles=[Role.admin, Role.common])
    def delete(self, uuid: UUID):
        self.service.delete(uuid=uuid, user_id=self.user.id)
        return jsonify(), 204
