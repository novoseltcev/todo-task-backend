from flask import Blueprint, request, make_response, jsonify

from . import service as file_service
from .schema import FileSchema


file_blueprint = Blueprint('file', __name__)
prefix = '/file/'


@file_blueprint.route(prefix + 'download', methods=['POST'])
def open_file():
    schema = FileSchema(only='id').load(request.json)
    id = schema['id']

    file_data = file_service.download(id=id)
    return make_response(file_data)


@file_blueprint.route(prefix, methods=['POST'])
def create():
    try:
        file = request.files['file']
        task = request.form['task']
    except Exception:
        raise ValueError("File hasn't been transfered from client")
    filename = file.filename
    request_json = {
        'task': task,
        'name': filename,
        'data': file.read()
    }
    schema = FileSchema(only=('name', 'task', 'data')).load(request_json)

    file_service.create(**schema)
    return jsonify(filename), 202


@file_blueprint.route(prefix, methods=['DELETE'])
def delete():
    schema = FileSchema(only='id').load(request.json)
    id = schema['id']

    filename = file_service.get_one(id)['name']
    file_service.delete(id)
    return jsonify(filename), 202
