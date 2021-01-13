#
# привязка маршрутов
# и определение логики взаимодействия на высоком уровне
# в зависимости от переданного json-объекта
#
from flask import request
from server.init_db import DB
from server import flask_app
from server.operation import *


@flask_app.route("/", methods=["GET"])
def get_processor():
    json = request.json
    if json is None:
        return rerender_page(DB)


@flask_app.route("/", methods=['POST'])
def post_processor():
    file = request.files.get('file')
    if file is not None:
        id_task = 1
        filename = file.filename
        data = file.read()
        return create_file(DB, id_task, filename, data)

    id_file = int(request.form.get('open_file', 0))
    if id_file != 0:
        return download_file(DB, id_file)

    json = request.json
    if 'name_task' in json:
        name_task = json["name_task"]
        return create_task(DB, name_task)

    if 'name_category' in json:
        name_category = json["name_category"]
        return create_category(DB, name_category)

    if 'id_category' in json:
        id_category = int(json['id_category'])
        return open_category(DB, id_category)

    if 'id_file' in json:
        id_file = int(json['id_file'])
        return download_file(DB, id_file)
    return raise_error("Invalid request")


@flask_app.route("/", methods=['PUT'])
def put_processor():
    json = request.json
    if 'id_task' in json:
        id_task = int(json['id_task'])
        if 'prev_status' in json:
            new_status = (int(json['prev_status']) + 1) % 2
            return update_task_status(DB, id_task, new_status)

        if 'new_id_category' in json:
            new_id_category = int(json['new_id_category'])
            return update_task_category(DB, id_task, new_id_category)

        if 'filename' in json and 'data' in json:
            filename = json['filename']
            data = json['data']
            return create_file(DB, id_task, filename, data)

    if 'destination_id' in json and 'source' in json:
        destination_id = int(json['destination_id'])
        source = json['source']
        return update_category_name(DB, destination_id, source)
    return raise_error("Invalid request")


@flask_app.route("/", methods=['DELETE'])
def delete_processor():
    json = request.json
    if 'id_task' in json:
        id_task = int(json['id_task'])
        if 'id_file' in json:
            id_file = int(json['id_file'])
            return delete_file(DB, id_task, id_file)
        return delete_task(DB, id_task)

    if 'id_category' in json:
        id_category = int(json['id_category'])
        return delete_category(DB, id_category)
    return raise_error("Invalid request")
