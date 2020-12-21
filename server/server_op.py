from sqlite3 import IntegrityError
from server.sqlite_db import SQLiteDB
from flask import request, render_template, abort, Flask


class ServerOperationOnDB:
    flask_app = Flask(__name__)

    def __init__(self, flask_app: Flask, storage: SQLiteDB):
        self.storage = storage
        self.flask_app = flask_app

    @flask_app.route("/")
    def index(self):
        return self.rerender_page(), 200

    @flask_app.route("/", methods=['POST'])
    def create_task(self):
        json = request.json
        if 'task_name' in json:
            task_name = json['task_name']
            self.storage.append_task(task_name)

    @flask_app.route("/", methods=['POST'])
    def create_category(self):
        json = request.json
        if 'category_name' in json:
            category_name = json['category_name']
            try:
                self.storage.append_category(category_name)
                self.storage.current_category = category_name
            except IntegrityError:
                return {"error": "value already exists"}

    # @app.route("/", methods=['POST'])
    # def open_category(self):
    #     json = request.json
    #     if 'category' in json and json.get('operation') == 'open':
    #         self.storage.current_category = json['category']

    @flask_app.route("/", methods=['PUT'])
    def update_task_status(self):
        json = request.json
        if 'task_id' in json and 'prev_status' in json:
            task_id = int(json['task_id'])
            new_status = (int(json['prev_status']) + 1) % 2
            self.storage.update_task_status(task_id, new_status)  # TODO

    @flask_app.route("/", methods=['PUT'])
    def update_task_category(self):
        json = request.json
        if 'task_id' in json and 'new_category_id' in json:
            task_id = int(json['task_id'])
            new_category_id = int(json['new_category_id'])
            self.storage.update_task_category(task_id, new_category_id)

    @flask_app.route("/", methods=['PUT'])
    def update_category(self):
        json = request.json
        if 'destination' in json and 'source_id' in json:
            destination = json['destination']
            source = int(json['source'])
            self.storage.rename_category(destination, source)

    @flask_app.route("/", methods=['DELETE'])
    def delete_task(self):
        json = request.json
        if 'task_id' in json:
            task_id = int(json['task_id'])
            self.storage.remove_task(task_id)

    @flask_app.route("/", methods=['DELETE'])
    def delete_category(self):
        json = request.json
        if 'category_id' in json:
            category_id = int(json['category_id'])
            self.storage.remove_category(category_id)

    def rerender_page(self):
        tasks, categories = self.storage.get_filtered_tasks(), self.storage.get_categories()
        return render_template("index.html", tasks=tasks, categories=categories)