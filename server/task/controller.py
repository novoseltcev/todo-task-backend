# Основной модуль, работа с http
from flask import request, session, Blueprint

from . import service


task_blueprint = Blueprint('task', __name__)


@task_blueprint.before_request
def check_json():
    json = request.json
    if not json:
        raise Exception("")


@task_blueprint.route("/", methods=['POST'])
def create():
    current_category = session.get('current_category', 1)
    return service.create_task(current_category, request.json)


@task_blueprint.route("/status", methods=['PUT'])
def edit_status():
    json = request.json
    if not json:
        raise Exception("")
    return service.update_status(request.json)


@task_blueprint.route("/title", methods=['PUT'])
def edit_title():
    return service.update_title(request.json)


@task_blueprint.route("/category", methods=['PUT'])
def edit_category():
    return service.update_category(request.json)


@task_blueprint.route("/", methods=['DELETE'])
def delete():
    return service.delete_task(request.json)
