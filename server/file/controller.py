from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.file import service as file_service
from server.file.service import FileSchema


file_blueprint = Blueprint('file', __name__)
prefix = '/file/'


@file_blueprint.route(prefix + 'download', methods=['POST'])
@jwt_required()
def open_file():
    id_user = get_jwt_identity()
    try:
        schema = FileSchema(only=('id', )).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = schema['id']
    file_data = file_service.download(id_user, id)
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
        schema['id_task'] = 1
    except ValueError or ValidationError as e:
        raise InvalidSchema(e.args[0])

    file_service.upload(id_user, **schema)
    return jsonify(filename=schema['name']), 202


@file_blueprint.route(prefix, methods=['DELETE'])
@jwt_required()
def delete():
    id_user = get_jwt_identity()
    try:
        schema = FileSchema(only=('id',)).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = schema['id']
    file = file_service.delete(id_user, id)
    print(file)
    return jsonify(file), 202
