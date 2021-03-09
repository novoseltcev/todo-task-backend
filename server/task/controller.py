# Основной модуль, работа с http
from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.task import service as task_service
from server.task.service import TaskSchema


task_blueprint = Blueprint('task', __name__)
prefix = '/task/'


@task_blueprint.route(prefix, methods=['POST'])
def create():
    try:
        schema = TaskSchema(only=('title', 'category_id', 'status')).load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = task_service.create(schema)
    schema['id'] = id
    return jsonify(schema), 201


@task_blueprint.route(prefix, methods=['PUT'])
def edit():
    try:
        schema = TaskSchema().load(request.json)
    except ValidationError:
        raise InvalidSchema()

    task_service.update(schema)
    return jsonify(schema), 202


@task_blueprint.route(prefix, methods=['DELETE'])
def delete():
    try:
        schema = TaskSchema(only=('id',)).load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = schema['id']
    response = task_service.delete(id)
    return jsonify(response), 202
