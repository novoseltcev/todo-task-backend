from flask import Blueprint, request, make_response, jsonify
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.file import service as file_service
from server.file.service import FileSchema


file_blueprint = Blueprint('file', __name__)
prefix = '/file/'


@file_blueprint.route(prefix + 'download', methods=['POST'])
def open_file():
    try:
        schema = FileSchema(only='id').load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = schema['id']
    file_data = file_service.download(id=id)
    return make_response(file_data)


@file_blueprint.route(prefix, methods=['POST'])
def create():
    try:
        file = request.files['file']
        request.json['name'] = file.filename
        request.json['data'] = file.read()
        schema = FileSchema(only=('name', 'task', 'data')).load(request.json)
    except ValueError or ValidationError:
        raise InvalidSchema()

    file_service.create(**schema)
    return jsonify(filename=schema['name']), 202


@file_blueprint.route(prefix, methods=['DELETE'])
def delete():
    try:
        schema = FileSchema(only='id').load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = schema['id']
    filename = file_service.delete(id)
    return jsonify(filename=filename), 202
