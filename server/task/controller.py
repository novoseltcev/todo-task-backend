# Основной модуль, работа с http
from flask import Blueprint, jsonify, request
from flask_login import login_required

from . import service as task_service
from .schema import TaskSchema


task_blueprint = Blueprint('task', __name__)
prefix = '/task/'


@task_blueprint.route(prefix, methods=['POST'])
def create():
    schema = TaskSchema(only=('title', 'category')).load(request.json)
    title = schema['title']
    category = schema['category']

    task_service.create(title=title, category=category)
    return jsonify(title), 201


@task_blueprint.route(prefix, methods=['PUT'])
def edit():
    schema = TaskSchema().load(request.json)
    id = schema['id']
    request_obj = {
        'id': id,
        'title': schema['title'],
        'status': schema['status'],
        'category': schema['category']
    }

    task_service.update(**request_obj)
    response = task_service.get_one(id=id)
    return jsonify(response), 202


@task_blueprint.route(prefix, methods=['DELETE'])
def delete():
    schema = TaskSchema(only=('id',)).load(request.json)
    id = schema['id']

    response = task_service.get_one(id=id)
    task_service.delete(id=id)
    return jsonify(response), 202
