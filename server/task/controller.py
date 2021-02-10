# Основной модуль, работа с http
from flask import request, session, Blueprint

from server.task import service


task_blueprint = Blueprint('task', __name__)


@task_blueprint.route("/", methods=['POST'])
def create():
    json = request.json
    title = json["title"]
    current_category = session.get('current_category', 1)
    return service.create_task(title, current_category)


@task_blueprint.route("/status", methods=['PUT'])
def edit_status():
    json = request.json
    id = json['id']
    return service.update_status(id)


@task_blueprint.route("/title", methods=['PUT'])
def edit_title():
    json = request.json
    id = json['id']
    title = json['title']
    return service.update_title(id, title)


@task_blueprint.route("/category", methods=['PUT'])
def edit_category():
    json = request.json
    id = json['id']
    category = json['category']
    return service.update_category(id, category)


@task_blueprint.route("/", methods=['DELETE'])
def delete():
    id = request.json['id']
    return service.delete_task(id)
