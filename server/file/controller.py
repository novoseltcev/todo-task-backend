from flask import Blueprint, request, make_response
from flask_apispec import use_kwargs

from . import service
from .schema import FileSchema
from server import docs


file_blueprint = Blueprint('file', __name__)


@file_blueprint.route("/download", methods=['POST'])
@use_kwargs(FileSchema(only=('id',)))
def open_file(**kwargs):
    if len(kwargs.items()) == 0:
        kwargs['id'] = int(request.form['id'])
    service_response = service.download_file(**kwargs)
    return make_response(service_response)


@file_blueprint.route("/", methods=['POST'])
def create():
    task = request.json['task']
    file = request.files['file']
    if file is None:
        raise ValueError("File hasn't been transfered from client")
    filename = file.filename
    data = file.read()
    json = {'task': task, 'name': filename, 'data': data}
    service.create_file(json)
    return 204


@file_blueprint.route("/", methods=['DELETE'])
@use_kwargs(FileSchema(only=('id',)))
def delete(**kwargs):
    service.delete_file(**kwargs)
    return 204


docs.register(create, blueprint=file_blueprint.name)
docs.register(delete, blueprint=file_blueprint.name)
