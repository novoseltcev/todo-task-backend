# Основной модуль, работа с http
from flask import Blueprint
from flask_apispec import use_kwargs

from .schema import TaskSchema
from . import service

from server import docs


task_blueprint = Blueprint('task', __name__)


@task_blueprint.route("/", methods=['POST'])
@use_kwargs(TaskSchema(only=('title', 'category')))
def create(**kwargs):
    service.create_task(**kwargs)
    return service.get_task(**kwargs), 201


@task_blueprint.route("/status", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id',)))
def edit_status(**kwargs):
    service.update_status(**kwargs)
    return service.get_task(**kwargs), 202


@task_blueprint.route("/title", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id', 'title',)))
def edit_title(**kwargs):
    service.update_title(**kwargs)
    return service.get_task(**kwargs), 202


@task_blueprint.route("/category", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id', 'category')))
def edit_category(**kwargs):
    service.update_category(**kwargs)
    return service.get_task(**kwargs), 202


@task_blueprint.route("/", methods=['DELETE'])
@use_kwargs(TaskSchema(only=('id',)))
def delete(**kwargs):
    response = service.get_task(**kwargs)
    service.delete_task(**kwargs)
    return response, 202


docs.register(create, blueprint=task_blueprint.name)
docs.register(edit_status, blueprint=task_blueprint.name)
docs.register(edit_category, blueprint=task_blueprint.name)
docs.register(edit_title, blueprint=task_blueprint.name)
docs.register(delete, blueprint=task_blueprint.name)
