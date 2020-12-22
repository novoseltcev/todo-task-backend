from flask import request
from server.init_db import DB
from server import flask_app
from server.operation import *


# current_category = 'None'


@flask_app.route("/", methods=["GET"])
def index():
    return rerender_page(DB)


@flask_app.route("/", methods=['POST'])
def post_processor():
    json = request.json
    if 'name_task' in json:
        name_task = json["name_task"]
        return create_task(DB, name_task)

    if 'name_category' in json:
        name_category = json["name_category"]
        return create_category(DB, name_category)
    return raise_error()


# TODO
    # @app.route("/", methods=['POST'])
    # def open_category(self):
    #     json = request.json
    #     if 'category' in json and json.get('operation') == 'open':
    #         self.storage.current_category = json['category']
# TODO


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
        else:
            return raise_error()

    if 'destination_id' in json and 'source' in json:
        destination_id = int(json['destination_id'])
        source = json['source']
        return update_category_name(DB, destination_id, source)
    return raise_error()


@flask_app.route("/", methods=['DELETE'])
def delete_processor():
    json = request.json
    if 'id_task' in json:
        id_task = int(json['id_task'])
        return delete_task(DB, id_task)

    if 'id_category' in json:
        id_category = int(json['id_category'])
        delete_category(DB, id_category)
    return raise_error()

