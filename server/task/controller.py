# Основной модуль, работа с http
from flask import request, session, Blueprint
from flask_apispec import use_kwargs
from .schema import TaskSchema

from . import service


task_blueprint = Blueprint('task', __name__)


@task_blueprint.before_request
def check_json():
    json = request.json
    if not json:
        raise Exception("")


@task_blueprint.route("/", methods=['POST'])
@use_kwargs(TaskSchema(only=('title',)))
def create(**kwargs):
    current_category = session['current_category']
    return service.create_task(current_category, **kwargs)


@task_blueprint.route("/status", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id',)))
def edit_status(**kwargs):
    return service.update_status(**kwargs)


@task_blueprint.route("/title", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id', 'title',)))
def edit_title(**kwargs):
    return service.update_title(**kwargs)


@task_blueprint.route("/category", methods=['PUT'])
@use_kwargs(TaskSchema(only=('id', 'category')))
def edit_category(**kwargs):
    return service.update_category(**kwargs)


@task_blueprint.route("/", methods=['DELETE'])
@use_kwargs(TaskSchema(only=('id',)))
def delete(**kwargs):
    return service.delete_task(**kwargs)
