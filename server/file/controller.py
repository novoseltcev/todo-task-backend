from flask import request, Blueprint, redirect

from . import service


file_blueprint = Blueprint('file', __name__)


def check_json(f):
    json = request.json
    if not json:
        raise Exception("")


@file_blueprint.route("/download", methods=['POST'])
def open_file():
    json = {'id': int(request.form['id'])}
    return service.download_file(json)


@file_blueprint.route("/", methods=['POST'])
def create_file():
    task = request.form["task"]
    file = request.files['file']
    if file is None:
        raise ValueError("File hasn't been transfered from client")
    filename = file.filename
    data = file.read()
    json = {'task': task, 'name': filename, 'data': data}
    service.create_file(json)
    return redirect('/')


@file_blueprint.route("/", methods=['DELETE'])
def delete_file():
    return service.delete_file(request.json)
