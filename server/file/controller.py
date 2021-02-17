from flask import request, Blueprint
from flask_apispec import use_kwargs

from . import service
from .schema import FileSchema


file_blueprint = Blueprint('file', __name__)


@file_blueprint.route("/download", methods=['POST'])
@use_kwargs(FileSchema(only=('id',)))
def open_file(**kwargs):
    if len(kwargs.items()) == 0:
        kwargs['id'] = int(request.form['id'])

    from pprint import pprint
    pprint(kwargs)

    return service.download_file(**kwargs)


@file_blueprint.route("/", methods=['POST'])
def create_file():
    task = request.form['task']
    file = request.files['file']
    if file is None:
        raise ValueError("File hasn't been transfered from client")
    filename = file.filename
    data = file.read()
    json = {'task': task, 'name': filename, 'data': data}
    return service.create_file(json)


@file_blueprint.route("/", methods=['DELETE'])
@use_kwargs(FileSchema(only=('id',)))
def delete_file(**kwargs):
    return service.delete_file(**kwargs)
