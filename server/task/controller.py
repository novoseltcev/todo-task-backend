# Основной модуль, работа с http
from flask import request, session
# from server.app import app as task_blueprint
from server.task import service, task_blueprint


@task_blueprint.route("/task", methods=['POST'])
def create_task():
    json = request.json
    name_task = json["name_task"]
    current_category = session.get('current_category', 1)
    return service.create_task(name_task, current_category)


@task_blueprint.route("/", methods=['PUT'])
def edit_task():
    json = request.json
    id_task = json['id_task']
    title = json['title']
    status = json['status']
    id_category = json['id_category']
    return service.update_task(id_task, title, status, id_category)  # TODO


@task_blueprint.route("/task", methods=['DELETE'])
def delete_task():
    id_task = request.json['id_task']
    return service.delete_task(id_task)
