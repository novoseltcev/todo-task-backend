from flask import request, Blueprint

from . import service


file_blueprint = Blueprint('file', __name__)


@file_blueprint.route("/download", methods=['POST'])
def open_file():
    json = request.json
    if json is not None:
        id = json['id']
    else:
        id = request.form['id']
    return service.download_file(id)


@file_blueprint.route("/", methods=['POST'])
def create_file():
    task = request.form["task"]
    file = request.files['file']
    if file is None:
        raise ValueError("File hasn't been transfered from client")
    filename = file.filename
    data = file.read()
    return service.create_file(filename, data, task)


@file_blueprint.route("/", methods=['DELETE'])
def delete_file():
    json = request.json
    id = json['id']
    return service.delete_file(id)
