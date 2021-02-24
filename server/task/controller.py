# Основной модуль, работа с http
from flask import Blueprint
from flask_apispec import use_kwargs

from . import service as task_service
from .schema import TaskSchema


task_blueprint = Blueprint('task', __name__)
prefix = '/task/'


@task_blueprint.route(prefix, methods=['POST'])
@use_kwargs(TaskSchema(only=('title', 'category')))
def create(**kwargs):
    request_obj = {
        'title': kwargs['title'],
        'category': kwargs['category']
    }
    task_service.create(**request_obj)
    return 204


@task_blueprint.route(prefix, methods=['PUT'])
@use_kwargs(TaskSchema)
def edit(**kwargs):
    request_obj = {
        'id': kwargs['id'],
        'title': kwargs['title'],
        'status': kwargs['status'],
        'category': kwargs['category']
    }
    task_service.update(**request_obj)
    return task_service.get_one(request_obj['id']), 202


@task_blueprint.route(prefix, methods=['DELETE'])
@use_kwargs(TaskSchema(only=('id',)))
def delete(**kwargs):
    request_obj = {'id': kwargs['id']}
    response = task_service.get_one(**request_obj)
    task_service.delete(**request_obj)
    return response, 202
