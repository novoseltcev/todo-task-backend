from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from server.errors.exc import InvalidSchema
from server.category import service as category_service
from server.category.service import CategorySchema


category_blueprint = Blueprint('category', __name__)
prefix = '/category/'


@category_blueprint.route(prefix + 'all', methods=['GET'])
@jwt_required()
def get():
    user_id = get_jwt_identity()
    response = category_service.get_all(user_id)
    return jsonify(response), 200


@category_blueprint.route(prefix, methods=['POST'])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    try:
        schema = CategorySchema(only=('name',)).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    name = schema['name']
    id = category_service.create(name, user_id)
    return jsonify(id=id, name=name), 201


@category_blueprint.route(prefix, methods=['PUT'])
@jwt_required()
def edit():
    user_id = get_jwt_identity()
    try:
        schema = CategorySchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    category_service.update(schema, user_id)
    return jsonify(schema), 202


@category_blueprint.route(prefix, methods=['DELETE'])
@jwt_required()
def delete():
    user_id = get_jwt_identity()
    try:
        schema = CategorySchema(only=('id',)).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = schema['id']
    response = category_service.delete(id, user_id)
    return jsonify(response), 202
