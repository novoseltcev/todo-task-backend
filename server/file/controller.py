from flask import request
from server.file import service
from flask import Blueprint


file_blueprint = Blueprint('file', __name__)


@file_blueprint.route("/get", methods=['POST'])
def open_file():
    json = request.json
    if json is not None:
        id_file = json['id_file']
    else:
        id_file = request.form['id_file']
    return service.download_file(id_file)


@file_blueprint.route("/", methods=['POST'])
def create_file():
    file = request.files['file']
    if file is not None:
        id_task = request.form["id_task"]
        filename = file.filename
        data = file.read()
        return service.create_file(filename, data, id_task)


@file_blueprint.route("/", methods=['DELETE'])
def delete_file():
    json = request.json
    id_file = json['id_file']
    path = json['path']
    return service.delete_file(id_file, path)
