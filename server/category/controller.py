from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.category import service as category_service
from server.category.service import CategorySchema


category_blueprint = Blueprint('category', __name__)
prefix = '/category/'


@category_blueprint.route(prefix + 'all', methods=['GET'])
def get():
    response = category_service.get_all()
    return jsonify(response), 200


@category_blueprint.route(prefix, methods=['POST'])
def create():
    try:
        schema = CategorySchema(only=('name',)).load(request.json)
    except ValidationError:
        raise InvalidSchema()

    name = schema['name']
    id = category_service.create(name)
    return jsonify(id=id, name=name), 201


@category_blueprint.route(prefix, methods=['PUT'])
def edit():
    try:
        schema = CategorySchema().load(request.json)
    except ValidationError:
        raise InvalidSchema()

    category_service.update(schema)
    return jsonify(schema), 202


@category_blueprint.route(prefix, methods=['DELETE'])
def delete():
    try:
        schema = CategorySchema(only=('id',)).load(request.json)
    except ValidationError:
        raise InvalidSchema()

    id = schema['id']
    response = category_service.delete(id)
    return jsonify(response), 202
