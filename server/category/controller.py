from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from server import BaseConfig
from server.errors.exc import InvalidSchema
from server.category import service as category_service
from server.category.service import CategorySchema
from server.jwt_auth import admin_required

category_blueprint = Blueprint('category', __name__)
prefix = '/category/'


@category_blueprint.route('/categories/')
@jwt_required()
def get():
    id_user = get_jwt_identity()
    response = category_service.get_all(id_user)
    return jsonify(response)


@category_blueprint.route('/admin/categories/')
@admin_required(BaseConfig.admin_roles)
def get_4_admin():
    try:
        id_user = CategorySchema(only=('id_user',)).load(request.json)['id_user']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = category_service.get_all(id_user)
    return jsonify(response), 201


@category_blueprint.route(prefix, methods=['POST'])
@jwt_required()
def create():
    id_user = get_jwt_identity()
    try:
        name = CategorySchema(only=('name',)).load(request.json)['name']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    id = category_service.create(id_user, name)
    return jsonify(id=id, name=name), 201


@category_blueprint.route(prefix, methods=['PUT'])
@jwt_required()
def edit():
    id_user = get_jwt_identity()
    try:
        schema = CategorySchema().load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    category_service.update(id_user, schema)
    return jsonify(schema), 202


@category_blueprint.route(prefix, methods=['DELETE'])
@jwt_required()
def delete():
    id_user = get_jwt_identity()
    try:
        id = CategorySchema(only=('id',)).load(request.json)['id']
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = category_service.delete(id_user, id)
    return jsonify(response), 202


@category_blueprint.route('/admin/category/', methods=['DELETE'])
@admin_required(BaseConfig.admin_roles)
def delete_4_admin():
    try:
        schema = CategorySchema(only=('id', 'id_user')).load(request.json)
    except ValidationError as e:
        raise InvalidSchema(e.args[0])

    response = category_service.delete(**schema)
    return jsonify(response), 202
