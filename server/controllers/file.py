from flask import Blueprint, request, make_response, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from server import BaseConfig
from server.errors.exc import InvalidSchema
from server.services.file import service as file_service
from server.services.file.service import FileSchema
from server.jwt_auth import admin_required
from server.async_tasks import s3_cloud

file_blueprint = Blueprint('file', __name__)
prefix = '/file/'


@file_blueprint.route(prefix + 'download', methods=['POST'])
@jwt_required()
def open_file():
    id_user = get_jwt_identity()
    try:
        id = FileSchema(only=('id', )).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    file = file_service.get_file(id_user, id)
    name = file['name']
    path = file['path']
    file_data = file_service.s3_download(name, path)
    return make_response(file_data)


@file_blueprint.route(prefix, methods=['POST'])
# @jwt_required()
def create():
    # id_user = get_jwt_identity()  # TODO - Vue.js not work
    id_user = 1
    try:
        file = request.files['file']
        data = file.read()
        schema = FileSchema(only=('name', 'data')).load({'name': file.filename, 'data': data})  # TODO-'id_task',
        # schema['id_task'] = request.json['id_task']
    except ValueError or ValidationError as e:
        raise InvalidSchema(e.args[0])

    id_task = 1
    name = schema['name']
    data = schema['data']
    path = file_service.generate_path(name)
    id = file_service.create(id_user, id_task, name, path, data)
    try:
        async_process = s3_cloud.upload.delay(path)
    except Exception as e:
        file_service.delete(id_user, id)
        raise e
    return jsonify(msg='Uploading ' + schema['name'], id=id, path=path, uuid=async_process.id), 202


@file_blueprint.route(prefix, methods=['DELETE'])
@jwt_required()
def delete():
    id_user = get_jwt_identity()
    try:
        id = FileSchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    file = file_service.delete(id_user, id)
    return jsonify(file), 202


@file_blueprint.route(prefix + 'uploading_status')
@jwt_required()
def uploading():  # TODO -
    id_user = get_jwt_identity()
    try:
        schema = FileSchema(only=('id', 'path', 'uuid')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    result = file_service.check_uploading(id_user, **schema)
    return jsonify(result)


@file_blueprint.route('/admin/file/', methods=['DELETE'])
@admin_required(BaseConfig.admin_roles)
def delete_4_admin():
    try:
        schema = FileSchema(only=('id', 'id_user')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = file_service.delete(**schema)
    return jsonify(response), 202
