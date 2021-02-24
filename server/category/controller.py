from flask import Blueprint, jsonify, request

from . import service as category_service
from .schema import CategorySchema


category_blueprint = Blueprint('category', __name__)
prefix = '/category/'


@category_blueprint.route(prefix + 'all', methods=['GET'])
def get():
    response = category_service.get_all()
    return jsonify(response), 200


@category_blueprint.route(prefix, methods=['POST'])
def create():
    schema = CategorySchema(only=('name',)).load(request.json)
    name = schema['name']

    category_service.create(name=name)
    response = category_service.get_by_name(name=name)
    return jsonify(response), 201


@category_blueprint.route(prefix, methods=['PUT'])
def edit():
    schema = CategorySchema().load(request.json)
    id = schema['id']
    name = schema['name']

    category_service.update(id=id, name=name)
    response = category_service.get_one(id=id)
    return jsonify(response), 202


@category_blueprint.route(prefix, methods=['DELETE'])
def delete():
    schema = CategorySchema(only=('id',)).load(request.json)
    id = schema['id']

    response = category_service.get_one(id=id)
    category_service.delete(id=id)
    return jsonify(response), 202
