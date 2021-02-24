from flask import Blueprint, jsonify
from flask_apispec import use_kwargs

from . import service as category_service
from .schema import CategorySchema


category_blueprint = Blueprint('category', __name__)
prefix = '/category/'


@category_blueprint.route(prefix + 'all', methods=['GET'])
def get():
    return jsonify(category_service.get_all()), 200


@category_blueprint.route(prefix, methods=['POST'])
@use_kwargs(CategorySchema(only=('name',)))
def create(**kwargs):
    request_obj = {'name': kwargs['name']}
    category_service.create(**request_obj)
    return category_service.get_by_name(**request_obj), 201


@category_blueprint.route(prefix, methods=['PUT'])
@use_kwargs(CategorySchema)
def edit(**kwargs):
    request_obj = {
        'id': kwargs['id'],
        'name': kwargs['name']
    }
    category_service.update(**request_obj)
    return category_service.get_one(request_obj['id']), 202


@category_blueprint.route(prefix, methods=['DELETE'])
@use_kwargs(CategorySchema(only=('id',)))
def delete(**kwargs):
    request_obj = {'id': kwargs['id']}
    response = category_service.get_one(**request_obj)
    category_service.delete(**request_obj)
    return response, 202
