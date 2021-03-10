# Основной модуль, работа с http
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.task import service as task_service
from server.task.service import TaskSchema


task_blueprint = Blueprint('task', __name__)
prefix = '/task/'


@task_blueprint.route(prefix, methods=['POST'])
@jwt_required()
def create():
    try:
        schema = TaskSchema(only=('title', 'category_id')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = task_service.create(schema)
    schema['id'] = id
    return jsonify(schema), 201


@task_blueprint.route(prefix, methods=['PUT'])
@jwt_required()
def edit():
    try:
        schema = TaskSchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    task_service.update(schema)
    return jsonify(schema), 202


@task_blueprint.route(prefix, methods=['DELETE'])
@jwt_required()
def delete():
    try:
        schema = TaskSchema(only=('id',)).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = schema['id']
    response = task_service.delete(id)
    return jsonify(response), 202
