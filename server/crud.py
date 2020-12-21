from flask import render_template, request
from server.init_db import DB
from server import flask_app
from server.operation import *


# current_category = 'None'


@flask_app.route("/", methods=['POST'])
def post_processor():
    json = request.json
    if 'task_name' in json:
        task_name = json["task_name"]
        return create_task(DB, task_name)

    if 'category_name' in json:
        category_name = json["category_name"]
        return create_category(DB, category_name)

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
    if 'task_id' in json:
        if 'prev_status' in json:
            task_id = int(json['task_id'])
            new_status = (int(json['prev_status']) + 1) % 2
            return update_task_status(DB, task_id, new_status)

        if 'new_category_id' in json:
            task_id = int(json['task_id'])
            new_category_id = int(json['new_category_id'])
            return update_task_category(DB, task_id, new_category_id)

        else:
            return raise_error()

    if 'destination' in json and 'source_id' in json:
        destination = json['destination']
        source_id = int(json['source_id'])
        return update_category(DB, destination, source_id)

    return raise_error()


@flask_app.route("/", methods=['DELETE'])
def delete_processor():
    json = request.json
    if 'task_id' in json:
        task_id = int(json['task_id'])
        return delete_task(DB, task_id)

    if 'category_id' in json:
        category_id = int(json['category_id'])
        delete_category(DB, category_id)

    return raise_error()


@flask_app.route("/")
def rerender_page():
    tasks, categories = DB.get_filtered_tasks(), DB.get_categories()
    return render_template("index.html", tasks=tasks, categories=categories), 200


def raise_error():
    return 404
