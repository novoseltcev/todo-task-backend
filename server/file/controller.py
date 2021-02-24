from flask import Blueprint, request, make_response, jsonify
from flask_apispec import use_kwargs

from . import service as file_service
from .schema import FileSchema


file_blueprint = Blueprint('file', __name__)
prefix = '/file/'


@file_blueprint.route(prefix + 'download', methods=['POST'])
@use_kwargs(FileSchema(only=('id',)))
def open_file(**kwargs):
    request_obj = {'id': kwargs['id']}
    service_response = file_service.download(**request_obj)
    return make_response(service_response)


@file_blueprint.route(prefix, methods=['POST'])
def create():
    try:
        file = request.files['file']
        task = request.form['task']
    except Exception:
        raise ValueError("File hasn't been transfered from client")

    request_obj = FileSchema(only=('name', 'task', 'data')).load({
        'task': task,
        'name': file.filename,
        'data': file.read(),
    })
    file_service.create(**request_obj)
    return jsonify(request_obj['name']), 202


@file_blueprint.route(prefix, methods=['DELETE'])
@use_kwargs(FileSchema(only=('id',)))
def delete(**kwargs):
    request_obj = {'id': kwargs['id']}
    response = file_service.get_one(**request_obj)
    file_service.delete(**request_obj)
    return jsonify(response['name']), 202
